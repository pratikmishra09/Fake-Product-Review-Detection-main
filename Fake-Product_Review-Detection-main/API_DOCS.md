# 📡 API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check API status and model availability.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true
}
```

---

### 2. Single Prediction
**POST** `/predict`

Predict if a single review is fake or real.

**Request:**
```json
{
  "review_text": "This product is amazing!"
}
```

**Response:**
```json
{
  "review_text": "This product is amazing!",
  "prediction": "REAL",
  "confidence": 0.89,
  "fake_probability": 0.11,
  "real_probability": 0.89
}
```

**Validation:**
- Text length: 5-5000 characters
- Rate limit: 100 requests per session

---

### 3. Batch Prediction
**POST** `/predict_batch`

Predict multiple reviews at once.

**Request:**
```json
{
  "reviews": [
    "Great product!",
    "Terrible quality.",
    "Amazing! Best ever!"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "review_text": "Great product!",
      "prediction": "REAL",
      "confidence": 0.85,
      "fake_probability": 0.15
    },
    ...
  ],
  "total": 3,
  "fake_count": 1
}
```

**Validation:**
- Maximum 100 reviews per batch
- Rate limit: 50 requests per session

---

### 4. Statistics
**GET** `/stats`

Get prediction statistics.

**Response:**
```json
{
  "total_predictions": 150,
  "fake_count": 23,
  "real_count": 127,
  "avg_confidence": 0.87,
  "min_confidence": 0.52,
  "max_confidence": 0.99,
  "low_confidence_count": 5
}
```

---

### 5. Drift Detection
**GET** `/drift`

Check for model drift.

**Response:**
```json
{
  "drift_detected": false,
  "message": "No drift detected"
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Model not loaded |

---

## Python Client Example

```python
import requests

# Single prediction
response = requests.post('http://localhost:5000/predict', json={
    'review_text': 'This product is amazing!'
})
print(response.json())

# Batch prediction
response = requests.post('http://localhost:5000/predict_batch', json={
    'reviews': ['Review 1', 'Review 2', 'Review 3']
})
print(response.json())

# Get statistics
response = requests.get('http://localhost:5000/stats')
print(response.json())
```

---

## JavaScript Client Example

```javascript
// Single prediction
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({review_text: 'This product is amazing!'})
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Security Features

- Input validation and sanitization
- Rate limiting
- XSS protection
- CORS enabled
- Request logging

---

## Monitoring

All predictions are logged to `logs/` directory with:
- Timestamp
- Review text (first 100 chars)
- Prediction result
- Confidence score

Metrics are saved to `monitoring/` directory daily.
