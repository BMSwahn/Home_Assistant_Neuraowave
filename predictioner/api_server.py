#!/usr/bin/env python3
"""
Migraine Prediction Service - REST API Server

This Flask server provides REST API endpoints to serve migraine predictions
to the frontend. It reads the prediction data from the JSON file created
by predict.py.

Usage:
    python api_server.py

    The server will start on http://localhost:5000

Endpoints:
    GET /prediction - Returns the current migraine prediction
    GET /health     - Health check endpoint
"""

import json
import os
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access


def get_data_file_path():
    """
    Get the path to the prediction JSON file.

    Returns:
        str: Absolute path to prediction.json
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data", "prediction.json")


def read_prediction():
    """
    Read the current prediction from the JSON file.

    Returns:
        dict: Prediction data or error message
    """
    json_path = get_data_file_path()

    if not os.path.exists(json_path):
        return {
            "error": "No prediction available",
            "message": "Run predict.py first to generate a prediction",
            "timestamp": int(time.time())
        }

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {
            "error": "Failed to read prediction",
            "message": str(e),
            "timestamp": int(time.time())
        }


@app.route('/prediction', methods=['GET'])
def get_prediction():
    """
    GET endpoint to retrieve the current migraine prediction.

    Returns:
        JSON response with prediction data
    """
    prediction_data = read_prediction()

    # Set appropriate status code
    status_code = 200 if "error" not in prediction_data else 404

    return jsonify(prediction_data), status_code


@app.route('/health', methods=['GET'])
def health_check():
    """
    GET endpoint for health checking the API.

    Returns:
        JSON response with service status
    """
    json_path = get_data_file_path()
    prediction_exists = os.path.exists(json_path)

    return jsonify({
        "status": "healthy",
        "service": "migraine_prediction_api",
        "timestamp": int(time.time()),
        "prediction_available": prediction_exists
    }), 200


@app.route('/', methods=['GET'])
def root():
    """
    Root endpoint providing API information.

    Returns:
        JSON response with available endpoints
    """
    return jsonify({
        "service": "Migraine Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/prediction": "GET - Retrieve current migraine prediction",
            "/health": "GET - Health check endpoint"
        },
        "usage": "Run predict.py to generate predictions, then query this API"
    }), 200


def main():
    """
    Start the Flask development server.
    """
    print("=" * 60)
    print("Migraine Prediction API Server")
    print("=" * 60)
    print()
    print("Starting server on http://localhost:5000")
    print()
    print("Available endpoints:")
    print("  GET  http://localhost:5000/prediction")
    print("  GET  http://localhost:5000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Run the Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


if __name__ == "__main__":
    main()
