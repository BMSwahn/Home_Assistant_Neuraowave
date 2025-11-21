import requests
import json
import time
import os
from datetime import datetime

# --- Configuration for Home Assistant ---
# Base URL for your Home Assistant instance.
# Falls back to "http://100.64.0.4:8123" if HA_URL environment variable is not set.
HOME_ASSISTANT_URL = os.getenv("HA_URL", "http://100.64.0.4:8123")

# Webhook IDs defined in your Home Assistant automations.
# These must exactly match the 'webhook_id' configured in Home Assistant.
WEBHOOK_ID_CRITICAL_MIGRAINE = "critical_migraine_webhook"
WEBHOOK_ID_MIGRAINE_WARNING = "migraine_warning_webhook"

# Probability thresholds (0-1) for triggering different alerts.
CRITICAL_THRESHOLD = 0.75  # Probability >= this will trigger a critical alert.
WARNING_THRESHOLD = 0.40   # Probability >= this (and < critical) will trigger a warning alert.

# --- Configuration for External Migraine API ---
# The URL of the external API that provides migraine probability data.
# Falls back to "http://100.64.0.15:5000/prediction" if EXTERNAL_API_URL environment variable is not set.
EXTERNAL_MIGRAINE_API_URL = os.getenv("EXTERNAL_API_URL", "http://100.64.0.15:5000/prediction")

# --- Headers for Webhook POST Requests ---
# For Home Assistant webhooks, the URL itself contains the "secret" ID,
# so an Authorization header with a Bearer token is not typically required.
WEBHOOK_HEADERS = {
    "Content-Type": "application/json",
}

def get_migraine_data_from_external_api() -> dict | None:
    """
    Fetches migraine probability data from the configured external API.

    It expects a JSON response with at least a 'migraine_probability' key.
    Example expected JSON structure:
    {
        "timestamp": 1732197000,
        "migraine_probability": 0.75,
        "source": "manual_input"
    }

    Returns:
        A dictionary containing the parsed data if successful and valid,
        otherwise None.
    """
    print(f"[{datetime.now().isoformat()}] Fetching data from external API: {EXTERNAL_MIGRAINE_API_URL}")
    response = None # Initialize response to None for error handling
    try:
        response = requests.get(EXTERNAL_MIGRAINE_API_URL, timeout=15)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        print(f"[{datetime.now().isoformat()}] Received data: {json.dumps(data, indent=2)}")

        # Validate the presence and type of 'migraine_probability'
        if "migraine_probability" not in data or not isinstance(data["migraine_probability"], (int, float)):
            print(f"[{datetime.now().isoformat()}] Error: 'migraine_probability' key missing or invalid type in API response.")
            return None
        
        # Validate the range of 'migraine_probability'
        probability = data["migraine_probability"]
        if not (0 <= probability <= 1):
             print(f"[{datetime.now().isoformat()}] Error: 'migraine_probability' value ({probability}) must be between 0 and 1.")
             return None

        return data
    except requests.exceptions.Timeout:
        print(f"[{datetime.now().isoformat()}] Error: Request to external API timed out after 15 seconds: {EXTERNAL_MIGRAINE_API_URL}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"[{datetime.now().isoformat()}] Error: Could not connect to external API at {EXTERNAL_MIGRAINE_API_URL}. Details: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().isoformat()}] Error fetching data from external API: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
        return None
    except json.JSONDecodeError:
        print(f"[{datetime.now().isoformat()}] Error: Failed to decode JSON from external API response. Raw response: {response.text if response else 'N/A'}")
        return None

def trigger_home_assistant_webhook(webhook_id: str, payload_data: dict) -> None:
    """
    Sends a POST request to the specified Home Assistant webhook endpoint.

    Args:
        webhook_id: The unique ID of the webhook defined in Home Assistant.
        payload_data: A dictionary to be sent as the JSON body of the POST request.
                      This data will be accessible in Home Assistant automations
                      via `trigger.json`.
    """
    webhook_url = f"{HOME_ASSISTANT_URL}/api/webhook/{webhook_id}"

    print(f"[{datetime.now().isoformat()}] Triggering Home Assistant webhook: '{webhook_id}' with payload: {json.dumps(payload_data)}")

    response = None
    try:
        response = requests.post(webhook_url, headers=WEBHOOK_HEADERS, json=payload_data, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"[{datetime.now().isoformat()}] Successfully triggered webhook '{webhook_id}' in Home Assistant!")
        # Home Assistant webhooks typically return an empty 200 OK response on success.
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().isoformat()}] Error triggering webhook '{webhook_id}' in Home Assistant: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

def main() -> None:
    """
    Main function to fetch migraine data and trigger Home Assistant webhooks.
    """
    print(f"[{datetime.now().isoformat()}] Starting migraine probability integration (using webhooks)...")

    migraine_data = get_migraine_data_from_external_api()

    if migraine_data:
        probability = migraine_data["migraine_probability"]
        # Use .get() with a default value for 'source' and 'timestamp'
        # in case these keys are occasionally missing from the external API response.
        source = migraine_data.get("source", "unknown")
        timestamp = migraine_data.get("timestamp", int(time.time())) # Use current time as fallback

        # Prepare the payload that will be sent to the Home Assistant webhook.
        # This data will be accessible via 'trigger.json' in your automations.
        webhook_payload = {
            "probability": probability,
            "source": source,
            "timestamp": timestamp,
            "integrator_run_time": datetime.now().isoformat(), # Add when the script ran
        }

        if probability >= CRITICAL_THRESHOLD:
            print(f"[{datetime.now().isoformat()}] Migraine probability {probability:.2f} is CRITICAL (>= {CRITICAL_THRESHOLD:.2f}).")
            trigger_home_assistant_webhook(WEBHOOK_ID_CRITICAL_MIGRAINE, webhook_payload)
        elif probability >= WARNING_THRESHOLD:
            print(f"[{datetime.now().isoformat()}] Migraine probability {probability:.2f} is WARNING (>= {WARNING_THRESHOLD:.2f}).")
            trigger_home_assistant_webhook(WEBHOOK_ID_MIGRAINE_WARNING, webhook_payload)
        else:
            print(f"[{datetime.now().isoformat()}] Migraine probability {probability:.2f} is low (below {WARNING_THRESHOLD:.2f}). No alert fired.")
            # Optional: You could trigger a "migraine_clear" webhook/event here
            # if you have an automation to reset lights or clear notifications.
    else:
        print(f"[{datetime.now().isoformat()}] Failed to retrieve valid migraine data. No webhooks triggered.")

if __name__ == "__main__":
    main()
