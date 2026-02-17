from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
import sys
from logger import PredictionLogger
from monitoring import ModelMonitor
from validation import InputValidator, rate_limit
from action_handler import ReviewActionHandler
from continuous_learning import ContinuousLearning

app = Flask(__name__)
CORS(app)

# Initialize components
logger = PredictionLogger()
monitor = ModelMonitor()
action_handler = ReviewActionHandler()
learning = ContinuousLearning()

# Load trained model and preprocessor
MODEL_PATH = 'models/svm.pkl'
PREPROCESSOR_PATH = 'models/preprocessor.pkl'

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("Model and preprocessor loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please train the model first: python main.py")
    model = None
    preprocessor = None

@app.route('/')
def home():
    return jsonify({
        'status': 'active',
        'message': 'Fake Review Detection API',
        'endpoints': {
            '/predict': 'POST - Predict single review',
            '/predict_batch': 'POST - Predict multiple reviews',
            '/health': 'GET - Health check'
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': model is not None,
        'preprocessor_loaded': preprocessor is not None
    })

@app.route('/predict', methods=['POST'])
@rate_limit(max_requests=100)
def predict():
    if model is None or preprocessor is None:
        return jsonify({'error': 'Model not loaded. Train model first: python main.py'}), 500
    
    data = request.json
    review_text = data.get('review_text', '')
    
    # Validate input
    valid, msg = InputValidator.validate_review_text(review_text)
    if not valid:
        return jsonify({'error': msg}), 400
    
    # Preprocess
    df = pd.DataFrame({'review_text': [review_text]})
    X, _ = preprocessor.prepare_data(df, fit=False)
    
    # Predict
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    result = {
        'review_text': review_text,
        'prediction': 'FAKE' if prediction == 1 else 'REAL',
        'confidence': float(max(probability)),
        'fake_probability': float(probability[1]),
        'real_probability': float(probability[0])
    }
    
    # Log prediction
    logger.log_prediction(review_text, result['prediction'], result['confidence'])
    monitor.track_prediction(result['confidence'], result['prediction'])
    
    return jsonify(result)

@app.route('/predict_batch', methods=['POST'])
@rate_limit(max_requests=50)
def predict_batch():
    if model is None or preprocessor is None:
        return jsonify({'error': 'Model not loaded. Train model first: python main.py'}), 500
    
    data = request.json
    reviews = data.get('reviews', [])
    
    # Validate input
    valid, msg = InputValidator.validate_batch(reviews)
    if not valid:
        return jsonify({'error': msg}), 400
    
    df = pd.DataFrame({'review_text': reviews})
    X, _ = preprocessor.prepare_data(df, fit=False)
    
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    results = []
    fake_count = 0
    for i, review in enumerate(reviews):
        pred = 'FAKE' if predictions[i] == 1 else 'REAL'
        if pred == 'FAKE':
            fake_count += 1
        results.append({
            'review_text': review,
            'prediction': pred,
            'confidence': float(max(probabilities[i])),
            'fake_probability': float(probabilities[i][1])
        })
    
    # Log batch
    logger.log_batch(len(reviews), fake_count, len(reviews) - fake_count)
    
    return jsonify({'results': results, 'total': len(results), 'fake_count': fake_count})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/stats')
def stats():
    """Get prediction statistics"""
    stats = monitor.get_statistics()
    if stats:
        return jsonify(stats)
    return jsonify({'message': 'No predictions yet'})

@app.route('/drift')
def drift():
    """Check for model drift"""
    has_drift, message = monitor.check_drift()
    return jsonify({'drift_detected': has_drift, 'message': message})

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit human feedback on prediction"""
    data = request.json
    review_text = data.get('review_text')
    predicted = data.get('predicted_label')
    actual = data.get('actual_label')
    confidence = data.get('confidence')
    
    feedback = learning.collect_feedback(review_text, predicted, actual, confidence)
    
    # Check if retraining needed
    needs_retrain, message = learning.check_retraining_needed()
    
    return jsonify({
        'feedback_recorded': True,
        'needs_retraining': needs_retrain,
        'message': message
    })

@app.route('/learning_stats')
def learning_stats():
    """Get continuous learning statistics"""
    stats = learning.get_learning_stats()
    if stats:
        return jsonify(stats)
    return jsonify({'message': 'No learning data available'})

@app.route('/action_stats')
def action_stats():
    """Get action statistics"""
    stats = action_handler.get_statistics()
    if stats:
        return jsonify(stats)
    return jsonify({'message': 'No actions recorded'})

@app.route('/flagged_reviews')
def flagged_reviews():
    """Get list of flagged reviews"""
    flagged = action_handler.get_flagged_reviews()
    return jsonify({'flagged_reviews': flagged, 'count': len(flagged)})
