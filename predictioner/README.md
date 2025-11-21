# Predictioner - Migraine Prediction Service Prototype

This is a **prototype** implementation of the migraine prediction service for the Home Assistant integration hackathon project. It simulates the prediction system that will eventually be replaced by a real ML model developed by the backend team.

## 🎯 Purpose

This prototype allows frontend development to proceed while the backend team develops the actual prediction model. It provides:

1. **Manual prediction input** via command-line interface
2. **REST API** to serve predictions to the frontend
3. **Data exploration tools** (prototype only) to understand available features

## 📁 Project Structure

```
predictioner/
├── predict.py          # Main script: manual input → JSON output
├── api_server.py       # Flask REST API to serve predictions
├── explore_data.py     # ⚠️ PROTOTYPE ONLY: explore synthetic data
├── requirements.txt    # Python dependencies
├── data/
│   └── prediction.json # Generated prediction output
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd predictioner
pip install -r requirements.txt
```

### 2. Generate a Prediction (Manual Input)

Run the prediction script and enter a float value between 0.0 and 1.0:

```bash
python predict.py
```

**Example:**
```
Enter migraine probability (0.0-1.0) or 'q' to quit: 0.75

✓ Prediction saved successfully!
  Probability: 75.0% (0.75)
  Saved to: c:\...\predictioner\data\prediction.json
```

This creates/updates the `data/prediction.json` file:

```json
{
  "migraine_probability": 0.75,
  "timestamp": 1732197000,
  "source": "manual_input"
}
```

### 3. Start the REST API Server

In a separate terminal, start the Flask server:

```bash
python api_server.py
```

The server will start on `http://localhost:5000`

### 4. Access the API

**Get Current Prediction:**
```bash
curl http://localhost:5000/prediction
```

Response:
```json
{
  "migraine_probability": 0.75,
  "timestamp": 1732197000,
  "source": "manual_input"
}
```

**Health Check:**
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "migraine_prediction_api",
  "timestamp": 1732197300,
  "prediction_available": true
}
```

### 5. (Optional) Explore Synthetic Data

⚠️ **WARNING: This is for prototype/demonstration only!**

```bash
python explore_data.py
```

This script explores the structure of the synthetic dataset to understand what features will be available for the real ML model. It does **NOT** make real predictions.

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/prediction` | GET | Get current migraine prediction |
| `/health` | GET | Health check endpoint |

## 📊 Data Format

### Prediction JSON Format

The prediction data is stored in `data/prediction.json`:

```json
{
  "migraine_probability": 0.75,
  "timestamp": 1732197000,
  "source": "manual_input"
}
```

**Fields:**
- `migraine_probability` (float): Value between 0.0 and 1.0 representing 0% to 100% chance
- `timestamp` (integer): Unix epoch timestamp (seconds since Jan 1, 1970) when prediction was made
- `source` (string): Source of prediction ("manual_input" in prototype)

## 🔄 Workflow

```
┌─────────────────┐
│   Frontend      │
│   Application   │
└────────┬────────┘
         │
         │ GET /prediction
         │
         ▼
┌─────────────────┐      reads      ┌──────────────────┐
│  api_server.py  │◄─────────────────│ prediction.json  │
└─────────────────┘                  └────────┬─────────┘
                                              │
                                              │ writes
                                              │
                                     ┌────────▼─────────┐
                                     │   predict.py     │
                                     │  (manual input)  │
                                     └──────────────────┘
```

### Current Prototype Flow:
1. Run `predict.py` to manually enter a prediction value
2. Value is saved to `data/prediction.json`
3. `api_server.py` serves this JSON via REST API
4. Frontend fetches prediction via GET request

### Future Production Flow:
1. Frontend sends user data to backend API
2. Backend calls your prediction service with user data
3. **Real ML model** (replacing predict.py) analyzes data and returns prediction
4. Backend forwards prediction to frontend

## 🎓 Understanding the Synthetic Data

The repository includes synthetic data in `../jsonpython/synthetic_data_10_000/`:

- **health_data_10000_365.csv** - Daily health records for 10,000 people over 365 days
  - Features: stress, sleep, hormones, meals, weather contributions
  - Target: migraine_probability (0.0-1.0), migraine (boolean)

- **person_data_10000.csv** - Person profiles with trigger susceptibilities
  - Demographics: gender, birthdate
  - Triggers: stress, hormones, sleep, weather, meals, medicine

- **weather_data.csv** - Historical weather data
  - Temperature, pressure, wind, precipitation, cloud cover, etc.

Use `explore_data.py` to see the data structure (remember: prototype only!).

## ⚠️ Important Notes

### This is a Prototype
- ✅ Use `predict.py` for manual input (current functionality)
- ✅ Use `api_server.py` to serve predictions to frontend
- ⚠️ `explore_data.py` is for understanding data structure only (NOT real predictions)
- 🔮 Real ML model will be developed by backend team

### Not Included (Future Development)
- ❌ Actual machine learning model
- ❌ Training pipeline
- ❌ User data integration
- ❌ Production-grade authentication/security
- ❌ Database storage
- ❌ Scalability features

### For Production Use
When the backend team develops the real prediction service:
1. Replace `predict.py` with actual ML model endpoint
2. Update `api_server.py` to call the real backend API
3. Add proper authentication and security
4. Implement Home Assistant integration protocol
5. Add error handling and monitoring

## 🛠️ Development

### Testing the API

You can test the API using curl, Postman, or your browser:

```bash
# Get prediction
curl http://localhost:5000/prediction

# Health check
curl http://localhost:5000/health

# API info
curl http://localhost:5000/
```

### Frontend Integration Example

```javascript
// Fetch current migraine prediction
async function getMigrainePrediction() {
  try {
    const response = await fetch('http://localhost:5000/prediction');
    const data = await response.json();

    if (response.ok) {
      console.log('Migraine probability:', data.migraine_probability);
      console.log('Timestamp (Unix):', data.timestamp);
      // Convert Unix timestamp to JavaScript Date if needed
      const date = new Date(data.timestamp * 1000);
      console.log('Timestamp (Date):', date.toISOString());
      return data.migraine_probability;
    } else {
      console.error('Error:', data.error);
      return null;
    }
  } catch (error) {
    console.error('Failed to fetch prediction:', error);
    return null;
  }
}
```

## 📝 Dependencies

- **Flask 3.0.0** - Web framework for REST API
- **flask-cors 4.0.0** - CORS support for frontend access
- **pandas 2.1.4** - Data processing (explore_data.py only)
- **python-dateutil 2.8.2** - Date/time handling

## 🤝 Team Integration

### For Frontend Developers
- Use the `/prediction` endpoint to get migraine predictions
- The API will be running on `http://localhost:5000` during development
- Prediction value is a float between 0.0 and 1.0

### For Backend Developers
- The JSON format in `data/prediction.json` shows expected output structure
- The synthetic data in `../jsonpython/synthetic_data_10_000/` is available for model training
- Replace `predict.py` with your actual ML model service
- Keep the same JSON output format for compatibility

## 📄 License

Hackathon project - check with organizers for license details.

## 🆘 Troubleshooting

**Problem:** API returns "No prediction available"
**Solution:** Run `predict.py` first to generate a prediction

**Problem:** Cannot find synthetic data files
**Solution:** Ensure you're in the correct directory and `../jsonpython/synthetic_data_10_000/` exists

**Problem:** Port 5000 already in use
**Solution:** Stop other services using port 5000 or modify the port in `api_server.py`

**Problem:** Module not found errors
**Solution:** Run `pip install -r requirements.txt` to install dependencies

---

**Happy Hacking! 🚀**
