# 🚀 Fake Review Detection System - Deployment Guide

## 📋 Project Structure
```
Product Dtct/
├── main.py                      # Training pipeline
├── app.py                       # Flask REST API
├── web_app.py                   # Streamlit web interface
├── data_preprocessing.py        # NLP preprocessing
├── model_training.py            # ML model training
├── model_evaluation.py          # Performance metrics
├── label_generator.py           # Synthetic label generation
├── test_api.py                  # API testing
├── requirements.txt             # Dependencies
├── Dockerfile                   # Docker configuration
└── models/                      # Saved models (after training)
```

## 🎯 Quick Start

### 1. Train the Model
```bash
python main.py
```

### 2. Run Web Interface (Streamlit)
```bash
streamlit run web_app.py
```
Access at: http://localhost:8501

### 3. Run REST API (Flask)
```bash
python app.py
```
Access at: http://localhost:5000

### 4. Test API
```bash
python test_api.py
```

## 🌐 Deployment Options

### Option 1: Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python main.py

# Run API
python app.py
```

### Option 2: Docker Deployment
```bash
# Build image
docker build -t fake-review-detector .

# Run container
docker run -p 5000:5000 fake-review-detector
```

### Option 3: AWS Deployment (EC2)
```bash
# SSH to EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Clone repository
git clone your-repo-url
cd Product\ Dtct

# Install dependencies
pip3 install -r requirements.txt

# Train model
python3 main.py

# Run with nohup
nohup python3 app.py &
```

### Option 4: Heroku Deployment
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 5: AWS Lambda + API Gateway
- Package code with dependencies
- Create Lambda function
- Set up API Gateway
- Deploy serverless

### Option 6: Azure App Service
```bash
az webapp up --name fake-review-detector --runtime PYTHON:3.9
```

## 📡 API Endpoints

### GET /health
Check API health status

### POST /predict
Predict single review
```json
{
  "review_text": "This product is amazing!"
}
```

### POST /predict_batch
Predict multiple reviews
```json
{
  "reviews": ["Review 1", "Review 2", "Review 3"]
}
```

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=production
export MODEL_PATH=models/svm.pkl
export PORT=5000
```

## 📊 Performance Metrics
- **Accuracy**: ~94%
- **Model**: SVM (RBF kernel)
- **Features**: 3000+ TF-IDF + 8 custom features
- **Processing**: ~100ms per review

## 🛡️ Security Best Practices
- Rate limiting on API endpoints
- Input validation and sanitization
- HTTPS in production
- API key authentication
- CORS configuration

## 📈 Monitoring & Logging
- Log all predictions
- Track API response times
- Monitor model performance
- Set up alerts for anomalies

## 🔄 CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          pip install -r requirements.txt
          python main.py
          # Deploy commands
```

## 📞 Support
For issues or questions, contact: your-email@example.com
