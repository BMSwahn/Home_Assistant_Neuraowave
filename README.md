# Home Assistant Migraine Integration

A hackathon project that integrates migraine prediction services with Home Assistant for automated health monitoring and alerts.

## 🎯 Project Overview

This project consists of three main components that work together to predict migraine likelihood and trigger Home Assistant automations:

1. **Predictioner** - Migraine prediction service (prototype)
2. **Home Assistant Integrator** - Webhook-based integration script
3. **Synthetic Data** - Training/testing dataset (10,000 people × 365 days)

## 📁 Repository Structure

```
Home_Assistant_Neuraowave/
├── predictioner/                    # Migraine prediction service
│   ├── predict.py                   # Manual prediction input (prototype)
│   ├── api_server.py                # REST API server (Flask)
│   ├── explore_data.py              # Data exploration tool (prototype only)
│   └── data/prediction.json         # Current prediction output
├── migraine_integrator_webhooks.py  # Home Assistant webhook integration
├── jsonpython/synthetic_data_10_000/# Synthetic health data
│   ├── health_data_10000_365.csv    # Daily health records
│   ├── person_data_10000.csv        # Person profiles & triggers
│   └── weather_data.csv             # Weather data
├── flake.nix                        # Nix development environment
└── README.md                        # This file
```

## 🚀 Quick Start

### 1. Set Up the Prediction Service

```bash
cd predictioner
pip install -r requirements.txt

# Terminal 1: Generate predictions (manual input for prototype)
python predict.py

# Terminal 2: Start the REST API
python api_server.py
```

The API will be available at `http://localhost:5000/prediction`

### 2. Configure Home Assistant Integration

Set environment variables:
```bash
export HA_URL="http://YOUR_HOME_ASSISTANT_IP:8123"
export EXTERNAL_API_URL="http://localhost:5000/prediction"
```

Run the integrator:
```bash
python migraine_integrator_webhooks.py
```

### 3. (Optional) Using Nix

```bash
nix develop  # Enters development shell with all dependencies
```

## 🔄 System Workflow

```
┌──────────────┐      Manual Input       ┌────────────────┐
│   predict.py │ ───────────────────────> │ prediction.json│
└──────────────┘      (0.0 - 1.0)        └────────┬───────┘
                                                   │
                                                   │ Serves
                                                   ▼
                                          ┌────────────────┐
                                          │ api_server.py  │
                                          │  (Flask API)   │
                                          └────────┬───────┘
                                                   │
                                                   │ GET /prediction
                                                   ▼
                                        ┌──────────────────────┐
                                        │ migraine_integrator  │
                                        │   _webhooks.py       │
                                        └──────────┬───────────┘
                                                   │
                           ┌───────────────────────┼───────────────────────┐
                           │                       │                       │
                    probability < 0.40      0.40 ≤ probability < 0.75  probability ≥ 0.75
                           │                       │                       │
                      No Alert                     ▼                       ▼
                                         ┌──────────────────┐    ┌──────────────────┐
                                         │ WARNING Webhook  │    │ CRITICAL Webhook │
                                         └────────┬─────────┘    └────────┬─────────┘
                                                  │                       │
                                                  └───────────┬───────────┘
                                                              │
                                                              ▼
                                                   ┌────────────────────┐
                                                   │  Home Assistant    │
                                                   │   Automations      │
                                                   │ (Lights, Alerts)   │
                                                   └────────────────────┘
```

## 📊 Data Format

### Prediction JSON
```json
{
  "migraine_probability": 0.75,
  "timestamp": 1732197000,
  "source": "manual_input"
}
```

### Webhook Payload to Home Assistant
```json
{
  "probability": 0.75,
  "source": "manual_input",
  "timestamp": 1732197000,
  "integrator_run_time": "2025-11-21T16:30:00.123456"
}
```

## 🎓 Components Explained

### Predictioner ([predictioner/](predictioner/))
**Prototype** prediction service that:
- Accepts manual input (0.0-1.0) representing migraine probability
- Stores predictions as JSON with Unix timestamps
- Serves predictions via REST API

> **Note:** This is a prototype using manual input. In production, this would be replaced by a real ML model trained on user health data.

### Home Assistant Integrator ([migraine_integrator_webhooks.py](migraine_integrator_webhooks.py))
Integration script that:
- Fetches predictions from the API every run
- Evaluates thresholds:
  - **CRITICAL** (≥ 0.75): Triggers critical alert webhook
  - **WARNING** (≥ 0.40): Triggers warning webhook
  - **LOW** (< 0.40): No action
- Sends data to Home Assistant webhooks for automation

### Synthetic Data ([jsonpython/synthetic_data_10_000/](jsonpython/synthetic_data_10_000/))
Dataset with 10,000 synthetic people and 365 days of health records including:
- **Health data**: stress, sleep, hormones, meals, weather impacts, migraine events
- **Person profiles**: demographics, trigger susceptibilities
- **Weather data**: temperature, pressure, precipitation, etc.

Use `predictioner/explore_data.py` to examine the data structure.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HA_URL` | Home Assistant URL | `http://100.64.0.4:8123` |
| `EXTERNAL_API_URL` | Prediction API URL | `http://100.64.0.15:5000/prediction` |

### Thresholds (in migraine_integrator_webhooks.py)

```python
CRITICAL_THRESHOLD = 0.75  # Trigger critical alert
WARNING_THRESHOLD = 0.40   # Trigger warning alert
```

### Webhook IDs

Configure these in Home Assistant automations to match:
```python
WEBHOOK_ID_CRITICAL_MIGRAINE = "tuva_eMDDtZzRZumbnQw34xL"
WEBHOOK_ID_MIGRAINE_WARNING = "tuva_eMDDtZzRZumbnQw34xL"
```

## 🔮 Future Development

### For Production:
- [ ] Replace manual input with real ML model
- [ ] Train model on actual user data
- [ ] Add user authentication and data privacy
- [ ] Implement continuous monitoring/scheduling
- [ ] Add database for prediction history
- [ ] Build Home Assistant custom integration component
- [ ] Add mobile app notifications

### Current Limitations:
- ⚠️ Prototype uses manual input, not real predictions
- ⚠️ No authentication/authorization
- ⚠️ Single-user system
- ⚠️ No persistence beyond latest prediction
- ⚠️ Manual execution (no scheduler)

## 📚 Documentation

- [Predictioner README](predictioner/README.md) - Detailed documentation for the prediction service
- [Synthetic Data Info](jsonpython/synthetic_data_10_000/) - Information about the dataset

## 🤝 Team Workflow

**Frontend Team**: Use `http://localhost:5000/prediction` to fetch migraine probabilities

**Backend/ML Team**: Replace `predictioner/predict.py` with actual ML model, maintain JSON format

**Home Assistant Team**: Configure webhooks and automations using the provided webhook IDs

## 📄 License

Hackathon project - check with organizers for license details.

---

**Built for Health & Wellbeing Hackathon** 🚀
