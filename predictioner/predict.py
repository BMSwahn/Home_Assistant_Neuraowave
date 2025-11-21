#!/usr/bin/env python3
"""
Migraine Prediction Service - Manual Input Script

This script simulates the prediction service by accepting manual float input.
In a production system, this would be replaced by an actual ML model that
receives data from the backend API and makes real predictions.

Usage:
    python predict.py

    Then enter a float value between 0.0 and 1.0 representing the migraine
    probability percentage (0.0 = 0%, 1.0 = 100%).
"""

import json
import os
import time


def validate_input(value_str):
    """
    Validate that the input is a float between 0.0 and 1.0.

    Args:
        value_str: String input from user

    Returns:
        float: Validated float value

    Raises:
        ValueError: If input is not valid
    """
    try:
        value = float(value_str)
        if not 0.0 <= value <= 1.0:
            raise ValueError("Value must be between 0.0 and 1.0")
        return value
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError("Input must be a valid number")
        raise


def save_prediction(migraine_probability):
    """
    Save the prediction to a JSON file.

    Args:
        migraine_probability: Float between 0.0 and 1.0

    Returns:
        str: Path to the saved JSON file
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Create prediction JSON
    prediction_data = {
        "migraine_probability": round(migraine_probability, 4),
        "timestamp": int(time.time()),
        "source": "manual_input"
    }

    # Save to JSON file
    json_path = os.path.join(data_dir, "prediction.json")
    with open(json_path, 'w') as f:
        json.dump(prediction_data, f, indent=2)

    return json_path


def main():
    """
    Main function to run the manual prediction input script.
    """
    print("=" * 60)
    print("Migraine Prediction Service - Manual Input")
    print("=" * 60)
    print()
    print("This script simulates the prediction service.")
    print("Enter a migraine probability as a float between 0.0 and 1.0")
    print("  0.0 = 0% chance of migraine")
    print("  1.0 = 100% chance of migraine")
    print()

    while True:
        try:
            # Get input from user
            user_input = input("Enter migraine probability (0.0-1.0) or 'q' to quit: ").strip()

            # Check if user wants to quit
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("\nExiting...")
                break

            # Validate and convert input
            migraine_probability = validate_input(user_input)

            # Save prediction
            json_path = save_prediction(migraine_probability)

            # Display success message
            print()
            print("✓ Prediction saved successfully!")
            print(f"  Probability: {migraine_probability:.1%} ({migraine_probability})")
            print(f"  Saved to: {json_path}")
            print()
            print("-" * 60)
            print()

        except ValueError as e:
            print(f"\n✗ Error: {e}")
            print("Please try again.\n")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
