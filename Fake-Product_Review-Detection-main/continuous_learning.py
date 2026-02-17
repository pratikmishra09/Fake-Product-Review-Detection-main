import pandas as pd
import joblib
from datetime import datetime
import os

class ContinuousLearning:
    """Handle continuous learning and model updates"""
    
    def __init__(self, feedback_dir='feedback', models_dir='models'):
        os.makedirs(feedback_dir, exist_ok=True)
        self.feedback_file = f"{feedback_dir}/feedback_{datetime.now().strftime('%Y%m')}.csv"
        self.models_dir = models_dir
        self.feedback_data = []
    
    def collect_feedback(self, review_text, predicted_label, actual_label, confidence):
        """Collect human feedback on predictions"""
        feedback = {
            'timestamp': datetime.now().isoformat(),
            'review_text': review_text,
            'predicted_label': predicted_label,
            'actual_label': actual_label,
            'confidence': confidence,
            'correct': predicted_label == actual_label
        }
        
        self.feedback_data.append(feedback)
        self._save_feedback()
        
        return feedback
    
    def _save_feedback(self):
        """Save feedback to CSV"""
        df = pd.DataFrame(self.feedback_data)
        
        if os.path.exists(self.feedback_file):
            existing = pd.read_csv(self.feedback_file)
            df = pd.concat([existing, df], ignore_index=True)
        
        df.to_csv(self.feedback_file, index=False)
    
    def check_retraining_needed(self, accuracy_threshold=0.85, min_samples=100):
        """Check if model needs retraining"""
        if not os.path.exists(self.feedback_file):
            return False, "No feedback data available"
        
        df = pd.read_csv(self.feedback_file)
        
        if len(df) < min_samples:
            return False, f"Insufficient feedback samples: {len(df)}/{min_samples}"
        
        accuracy = df['correct'].mean()
        
        if accuracy < accuracy_threshold:
            return True, f"Accuracy dropped to {accuracy:.2%}, retraining needed"
        
        return False, f"Model performing well: {accuracy:.2%}"
    
    def retrain_model(self, preprocessor, model_trainer):
        """Retrain model with new feedback data"""
        print("🔄 Starting model retraining...")
        
        # Load feedback data
        df = pd.read_csv(self.feedback_file)
        df['label'] = df['actual_label'].map({'FAKE': 1, 'REAL': 0})
        
        # Preprocess
        X, _ = preprocessor.prepare_data(df, fit=True)
        y = df['label']
        
        # Retrain
        trained_models = model_trainer.train_all(X, y)
        
        # Save updated models
        model_trainer.save_models()
        joblib.dump(preprocessor, f'{self.models_dir}/preprocessor.pkl')
        
        print(f"✅ Model retrained with {len(df)} samples")
        
        # Archive old feedback
        archive_file = self.feedback_file.replace('.csv', f'_archived_{datetime.now().strftime("%Y%m%d")}.csv')
        os.rename(self.feedback_file, archive_file)
        
        return trained_models
    
    def detect_new_patterns(self):
        """Detect emerging spam patterns"""
        if not os.path.exists(self.feedback_file):
            return []
        
        df = pd.read_csv(self.feedback_file)
        
        # Find reviews that were incorrectly classified
        incorrect = df[df['correct'] == False]
        
        if len(incorrect) == 0:
            return []
        
        # Analyze patterns in misclassified reviews
        patterns = {
            'high_confidence_errors': len(incorrect[incorrect['confidence'] > 0.8]),
            'false_positives': len(incorrect[incorrect['predicted_label'] == 'FAKE']),
            'false_negatives': len(incorrect[incorrect['predicted_label'] == 'REAL']),
            'total_errors': len(incorrect)
        }
        
        return patterns
    
    def get_learning_stats(self):
        """Get continuous learning statistics"""
        if not os.path.exists(self.feedback_file):
            return None
        
        df = pd.read_csv(self.feedback_file)
        
        stats = {
            'total_feedback': len(df),
            'accuracy': df['correct'].mean(),
            'avg_confidence': df['confidence'].mean(),
            'false_positives': len(df[(df['predicted_label'] == 'FAKE') & (df['actual_label'] == 'REAL')]),
            'false_negatives': len(df[(df['predicted_label'] == 'REAL') & (df['actual_label'] == 'FAKE')]),
            'last_updated': df['timestamp'].max()
        }
        
        return stats
