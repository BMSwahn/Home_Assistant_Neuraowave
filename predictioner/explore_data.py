#!/usr/bin/env python3
"""
⚠️  PROTOTYPE/DEMONSTRATION SCRIPT ONLY - NOT FOR PRODUCTION ⚠️

Migraine Data Exploration Script

This script is ONLY for exploring the synthetic dataset structure and
demonstrating what features are available. It does NOT make real predictions
and should NOT be used in production.

Purpose:
- Understand the structure of the synthetic data
- See what features exist (stress, sleep, hormones, weather, etc.)
- Demonstrate the data format for future ML model development

This is a PROTOTYPE tool to help understand what data the real backend
team will work with when building the actual prediction model.

Usage:
    python explore_data.py
"""

import os
import sys
import pandas as pd
from datetime import datetime


def print_warning():
    """
    Print prominent warning that this is prototype code only.
    """
    print()
    print("=" * 70)
    print("⚠️  WARNING: PROTOTYPE/DEMONSTRATION ONLY ⚠️".center(70))
    print("=" * 70)
    print()
    print("This script is for EXPLORING DATA STRUCTURE ONLY.")
    print("It does NOT make real predictions!")
    print()
    print("The actual prediction model will be developed by the backend team")
    print("using real user data and proper machine learning techniques.")
    print()
    print("=" * 70)
    print()


def get_data_paths():
    """
    Get paths to the synthetic data files.

    Returns:
        dict: Paths to data files
    """
    # Navigate from predictioner/ to jsonpython/synthetic_data_10_000/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    data_dir = os.path.join(repo_root, "jsonpython", "synthetic_data_10_000")

    return {
        "health_data": os.path.join(data_dir, "health_data_10000_365.csv"),
        "person_data": os.path.join(data_dir, "person_data_10000.csv"),
        "weather_data": os.path.join(data_dir, "weather_data.csv")
    }


def check_files_exist(paths):
    """
    Check if data files exist.

    Args:
        paths: Dictionary of file paths

    Returns:
        bool: True if all files exist
    """
    all_exist = True
    for name, path in paths.items():
        if not os.path.exists(path):
            print(f"✗ Missing file: {name}")
            print(f"  Expected at: {path}")
            all_exist = False
        else:
            print(f"✓ Found: {name}")

    return all_exist


def explore_health_data(file_path, num_samples=5):
    """
    Explore the health data CSV file.

    Args:
        file_path: Path to health_data CSV
        num_samples: Number of sample rows to display
    """
    print("\n" + "=" * 70)
    print("HEALTH DATA EXPLORATION (Synthetic Dataset)")
    print("=" * 70)

    try:
        # Read only a subset for quick exploration
        print("\nLoading health data (this may take a moment)...")
        df = pd.read_csv(file_path, nrows=10000)  # Read first 10k rows for speed

        print(f"\n✓ Loaded {len(df):,} sample rows")
        print(f"\nTotal columns: {len(df.columns)}")
        print("\nColumn names and types:")
        print("-" * 70)
        for col in df.columns:
            dtype = df[col].dtype
            print(f"  {col:<30} {str(dtype):<15}")

        print("\n" + "-" * 70)
        print(f"Sample records (first {num_samples} rows):")
        print("-" * 70)
        print(df.head(num_samples).to_string())

        print("\n" + "-" * 70)
        print("Migraine Probability Statistics:")
        print("-" * 70)
        if 'migraine_probability' in df.columns:
            print(df['migraine_probability'].describe())

            print("\nMigraine occurrence rate:")
            if 'migraine' in df.columns:
                migraine_rate = df['migraine'].sum() / len(df) * 100
                print(f"  {migraine_rate:.2f}% of records show migraine occurrence")

        print("\n" + "-" * 70)
        print("Available features for prediction:")
        print("-" * 70)
        features = [
            "stress_intensity (0-5 scale)",
            "sleep_duration (minutes)",
            "sleep_deficit (boolean)",
            "missed_meal (boolean)",
            "menstruation (boolean)",
            "delivery (boolean)",
            "Weather contribution factors (p_weather)",
        ]
        for feature in features:
            print(f"  • {feature}")

    except Exception as e:
        print(f"\n✗ Error loading health data: {e}")


def explore_person_data(file_path, num_samples=5):
    """
    Explore the person data CSV file.

    Args:
        file_path: Path to person_data CSV
        num_samples: Number of sample rows to display
    """
    print("\n" + "=" * 70)
    print("PERSON DATA EXPLORATION (Synthetic Dataset)")
    print("=" * 70)

    try:
        df = pd.read_csv(file_path)

        print(f"\n✓ Loaded {len(df):,} person records")
        print(f"\nTotal columns: {len(df.columns)}")

        print("\n" + "-" * 70)
        print(f"Sample records (first {num_samples} rows):")
        print("-" * 70)
        print(df.head(num_samples).to_string())

        print("\n" + "-" * 70)
        print("Migraine Frequency Distribution:")
        print("-" * 70)
        if 'migraine_days_per_month' in df.columns:
            print(df['migraine_days_per_month'].value_counts().sort_index())

        print("\n" + "-" * 70)
        print("Trigger Susceptibility Ranges:")
        print("-" * 70)
        trigger_cols = [col for col in df.columns if col.startswith('trigger_')]
        for col in trigger_cols:
            if col in df.columns:
                print(f"  {col:<25} Min: {df[col].min():.3f}  Max: {df[col].max():.3f}  Mean: {df[col].mean():.3f}")

    except Exception as e:
        print(f"\n✗ Error loading person data: {e}")


def main():
    """
    Main function to run data exploration.
    """
    print_warning()

    print("Checking for synthetic data files...")
    print("-" * 70)

    paths = get_data_paths()

    if not check_files_exist(paths):
        print("\n✗ Cannot proceed - missing data files")
        print("\nExpected data location:")
        print("  jsonpython/synthetic_data_10_000/")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Starting Data Exploration")
    print("=" * 70)

    # Explore health data
    explore_health_data(paths["health_data"])

    # Explore person data
    explore_person_data(paths["person_data"])

    # Final reminder
    print("\n" + "=" * 70)
    print("⚠️  REMINDER: This is PROTOTYPE exploration only ⚠️")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  • The synthetic data contains rich features for prediction")
    print("  • Real predictions require ML model training (not done here)")
    print("  • Use predict.py for manual input in the prototype system")
    print("  • Backend team will develop the real prediction model")
    print()


if __name__ == "__main__":
    main()
