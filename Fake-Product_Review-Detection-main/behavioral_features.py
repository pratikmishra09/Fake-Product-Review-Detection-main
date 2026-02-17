import pandas as pd
from datetime import datetime

class BehavioralFeatureExtractor:
    """Extract behavioral features from review metadata"""
    
    def __init__(self):
        self.user_history = {}
    
    def extract_review_frequency(self, df):
        """Calculate reviews per user"""
        if 'user_id' in df.columns:
            df['review_frequency'] = df.groupby('user_id')['user_id'].transform('count')
        else:
            df['review_frequency'] = 1
        return df
    
    def extract_rating_deviation(self, df):
        """Calculate how much user's rating deviates from product average"""
        if 'rating' in df.columns and 'product_id' in df.columns:
            product_avg = df.groupby('product_id')['rating'].transform('mean')
            df['rating_deviation'] = abs(df['rating'] - product_avg)
        else:
            df['rating_deviation'] = 0
        return df
    
    def detect_burst_activity(self, df):
        """Detect if user posted multiple reviews in short time"""
        if 'user_id' in df.columns and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.sort_values(['user_id', 'timestamp'])
            df['time_diff'] = df.groupby('user_id')['timestamp'].diff().dt.total_seconds()
            df['burst_activity'] = (df['time_diff'] < 3600).astype(int)  # < 1 hour
        else:
            df['burst_activity'] = 0
        return df
    
    def extract_account_age(self, df):
        """Calculate account age in days"""
        if 'account_created' in df.columns:
            df['account_created'] = pd.to_datetime(df['account_created'], errors='coerce')
            df['account_age_days'] = (datetime.now() - df['account_created']).dt.days
            df['new_account'] = (df['account_age_days'] < 30).astype(int)
        else:
            df['account_age_days'] = 365
            df['new_account'] = 0
        return df
    
    def extract_verified_purchase(self, df):
        """Check if purchase is verified"""
        if 'verified_purchase' in df.columns:
            df['is_verified'] = df['verified_purchase'].astype(int)
        else:
            df['is_verified'] = 0
        return df
    
    def extract_all_behavioral_features(self, df):
        """Extract all behavioral features"""
        df = self.extract_review_frequency(df)
        df = self.extract_rating_deviation(df)
        df = self.detect_burst_activity(df)
        df = self.extract_account_age(df)
        df = self.extract_verified_purchase(df)
        return df
