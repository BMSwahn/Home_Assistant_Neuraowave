import requests
import json
import time
import os
from datetime import datetime

# Home Assistant Config
HOME_ASSISTANT_URL = os.getenv("HA_URL", "http://100.64.0.4:8123")

# Webhook IDs defined in your Home Assistant automations
WEBHOOK_ID_CRITICAL_MIGRAINE = "critical_migraine_webhook"
WEBHOOK_ID_MIGRAINE_WARNING = "migraine_warning_webhook"

# Probability thresholds (0-1)
CRITICAL_THRESHOLD = 0.75 # Above this, trigger critical alert
WARNING_THRESHOLD = 0.40 # Above this, trigger warning (if not critical)

# --- Configuration for External Migraine API ---
# Replace with the actual URL of your external API
# This is a placeholder, ensure it returns data in the specified format.
EXTERNAL_MIGRAINE_API_URL = "http://100.64.0.15:5000/prediction" # Example URL

# --- Common Headers for Webhook POST Request ---
# Note: No Authorization header needed for webhooks, as the URL itself is the "secret"
WEBHOOK_HEADERS = {
    "Content-Type": "application/json",
}

def get_migraine_data_from_external_api():
    """
    Fetches migraine probability data from the external API.
    Expects a JSON response like:
    {
        "timestamp": 1678886400,
        "migraine_probability": 0.85,
        "source": "manual"
    }
    """
    print(f"Fetching data from external API: {EXTERNAL_MIGRAINE_API_URL}")
    try:
        response = requests.get(EXTERNAL_MIGRAINE_API_URL, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"Received data: {json.dumps(data, indent=2)}")

        # Validate expected keys
        if "migraine_probability" not in data or not isinstance(data["migraine_probability"], (int, float)):
            print("Error: 'migraine_probability' missing or invalid in external API response.")
            return None
        if not (0 <= data["migraine_probability"] <= 1):
             print("Error: 'migraine_probability' must be between 0 and 1.")
             return None

        return data
    except requests.exceptions.Timeout:
        print(f"Error: Request to external API timed out after 15 seconds: {EXTERNAL_MIGRAINE_API_URL}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to external API at {EXTERNAL_MIGRAINE_API_URL}. Details: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from external API: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
        return None

def trigger_home_assistant_webhook(webhook_id: str, payload_data: dict):
    """
    Sends a POST request to the Home Assistant webhook.
    """
    webhook_url = f"{HOME_ASSISTANT_URL}/api/webhook/{webhook_id}"

    print(f"Triggering Home Assistant webhook: '{webhook_id}' with payload: {json.dumps(payload_data)}")

    try:
        response = requests.post(webhook_url, headers=WEBHOOK_HEADERS, json=payload_data, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully triggered webhook '{webhook_id}' in Home Assistant!")
        # Webhooks typically return an empty 200 OK response if successful.
    except requests.exceptions.RequestException as e:
        print(f"Error triggering webhook '{webhook_id}' in Home Assistant: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

def main():
    print("Starting migraine probability integration (using webhooks)...")

    migraine_data = get_migraine_data_from_external_api()

    if migraine_data:
        probability = migraine_data["migraine_probability"]
        source = migraine_data.get("source", "unknown")
        timestamp = migraine_data.get("timestamp", int(time.time()))
        
        # Prepare payload for the webhook
        webhook_payload = {
            "probability": probability,
            "source": source,
            "timestamp": timestamp,
            "integrator_run_time": datetime.now().isoformat()
        }

        if probability >= CRITICAL_THRESHOLD:
            print(f"Migraine probability {probability:.2f} is CRITICAL (>= {CRITICAL_THRESHOLD:.2f}).")
            trigger_home_assistant_webhook(WEBHOOK_ID_CRITICAL_MIGRAINE, webhook_payload)
        elif probability >= WARNING_THRESHOLD:
            print(f"Migraine probability {probability:.2f} is WARNING (>= {WARNING_THRESHOLD:.2f}).")
            trigger_home_assistant_webhook(WEBHOOK_ID_MIGRAINE_WARNING, webhook_payload)
        else:
            print(f"Migraine probability {probability:.2f} is low (below {WARNING_THRESHOLD:.2f}). No alert fired.")
    else:
        print("Failed to retrieve valid migraine data. No webhooks triggered.")

if __name__ == "__main__":
    main()
