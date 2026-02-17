import logging
from datetime import datetime
import json
import os

class PredictionLogger:
    def __init__(self, log_dir='logs'):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = f"{log_dir}/predictions_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def log_prediction(self, review_text, prediction, confidence, source='api'):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'review_text': review_text[:100],  # First 100 chars
            'prediction': prediction,
            'confidence': confidence
        }
        self.logger.info(json.dumps(log_data))
    
    def log_batch(self, batch_size, fake_count, real_count):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'type': 'batch',
            'total': batch_size,
            'fake': fake_count,
            'real': real_count
        }
        self.logger.info(json.dumps(log_data))
