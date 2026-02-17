import re
from functools import wraps
from flask import request, jsonify

class InputValidator:
    @staticmethod
    def validate_review_text(text):
        """Validate review text input"""
        if not text or not isinstance(text, str):
            return False, "Review text must be a non-empty string"
        
        if len(text) < 5:
            return False, "Review text too short (minimum 5 characters)"
        
        if len(text) > 5000:
            return False, "Review text too long (maximum 5000 characters)"
        
        # Check for malicious patterns
        dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=']
        if any(pattern in text.lower() for pattern in dangerous_patterns):
            return False, "Invalid characters detected"
        
        return True, "Valid"
    
    @staticmethod
    def validate_batch(reviews):
        """Validate batch of reviews"""
        if not isinstance(reviews, list):
            return False, "Reviews must be a list"
        
        if len(reviews) == 0:
            return False, "Reviews list cannot be empty"
        
        if len(reviews) > 100:
            return False, "Maximum 100 reviews per batch"
        
        for review in reviews:
            valid, msg = InputValidator.validate_review_text(review)
            if not valid:
                return False, f"Invalid review: {msg}"
        
        return True, "Valid"

def rate_limit(max_requests=100):
    """Simple rate limiting decorator"""
    request_counts = {}
    
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr
            current_count = request_counts.get(client_ip, 0)
            
            if current_count >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            request_counts[client_ip] = current_count + 1
            return f(*args, **kwargs)
        return wrapped
    return decorator
