import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class ModelMonitor:
    def __init__(self, monitor_dir='monitoring'):
        os.makedirs(monitor_dir, exist_ok=True)
        self.monitor_file = f"{monitor_dir}/metrics_{datetime.now().strftime('%Y%m%d')}.json"
        self.predictions = []
    
    def track_prediction(self, confidence, prediction):
        self.predictions.append({
            'timestamp': datetime.now().isoformat(),
            'confidence': confidence,
            'prediction': prediction
        })
    
    def get_statistics(self):
        if not self.predictions:
            return None
        
        df = pd.DataFrame(self.predictions)
        stats = {
            'total_predictions': len(df),
            'fake_count': sum(df['prediction'] == 'FAKE'),
            'real_count': sum(df['prediction'] == 'REAL'),
            'avg_confidence': df['confidence'].mean(),
            'min_confidence': df['confidence'].min(),
            'max_confidence': df['confidence'].max(),
            'low_confidence_count': sum(df['confidence'] < 0.7)
        }
        return stats
    
    def save_metrics(self):
        stats = self.get_statistics()
        if stats:
            with open(self.monitor_file, 'w') as f:
                json.dump(stats, f, indent=2)
            return stats
        return None
    
    def check_drift(self, expected_fake_ratio=0.15, threshold=0.1):
        """Check if prediction distribution has drifted"""
        stats = self.get_statistics()
        if not stats or stats['total_predictions'] < 100:
            return False, "Insufficient data"
        
        actual_fake_ratio = stats['fake_count'] / stats['total_predictions']
        drift = abs(actual_fake_ratio - expected_fake_ratio)
        
        if drift > threshold:
            return True, f"Drift detected: {drift:.2%} deviation"
        return False, "No drift detected"
