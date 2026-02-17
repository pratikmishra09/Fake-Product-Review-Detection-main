import pandas as pd
import re
from textblob import TextBlob

class SyntheticLabelGenerator:
    def __init__(self):
        self.fake_indicators = 0
    
    def detect_duplicate_reviews(self, df):
        """Mark duplicate review texts as fake"""
        df['is_duplicate'] = df.duplicated(subset=['review_text'], keep=False).astype(int)
        return df
    
    def detect_rating_sentiment_mismatch(self, df):
        """Detect mismatch between rating and sentiment"""
        df['sentiment_score'] = df['review_text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        
        # High rating (4-5) with negative sentiment = fake
        # Low rating (1-2) with positive sentiment = fake
        df['rating_mismatch'] = 0
        df.loc[(df['rating'] >= 4) & (df['sentiment_score'] < -0.2), 'rating_mismatch'] = 1
        df.loc[(df['rating'] <= 2) & (df['sentiment_score'] > 0.2), 'rating_mismatch'] = 1
        return df
    
    def detect_suspicious_patterns(self, df):
        """Detect overly short/generic reviews"""
        df['word_count'] = df['review_text'].apply(lambda x: len(str(x).split()))
        df['char_count'] = df['review_text'].apply(lambda x: len(str(x)))
        
        # Very short reviews with extreme ratings
        df['suspicious_short'] = 0
        df.loc[(df['word_count'] < 5) & ((df['rating'] == 5) | (df['rating'] == 1)), 'suspicious_short'] = 1
        
        # Overly long reviews (spam)
        df.loc[df['word_count'] > 200, 'suspicious_short'] = 1
        
        # Generic phrases (common in fake reviews)
        generic_phrases = ['highly recommend', 'best product', 'worst purchase', 'amazing product', 
                          'terrible experience', 'love it', 'hate it', 'perfect', 'awful', 'exactly what i needed']
        df['has_generic'] = df['review_text'].apply(
            lambda x: 1 if any(phrase in str(x).lower() for phrase in generic_phrases) else 0
        )
        
        # Repetitive words
        df['repetitive'] = df['review_text'].apply(
            lambda x: 1 if len(set(str(x).lower().split())) < len(str(x).split()) * 0.5 else 0
        )
        
        return df
    
    def detect_excessive_caps(self, df):
        """Detect reviews with excessive capitalization"""
        df['excessive_caps'] = df['review_text'].apply(
            lambda x: 1 if sum(1 for c in str(x) if c.isupper()) > len(str(x)) * 0.3 else 0
        )
        return df
    
    def generate_labels(self, df, sample_size=200000):
        """Generate fake/real labels based on multiple heuristics"""
        print(f"Original dataset: {len(df)} reviews")
        print(f"Sampling {sample_size} reviews for training...")
        
        # Sample for faster processing (remove this line for full dataset)
        df = df.sample(n=min(sample_size, len(df)), random_state=42).reset_index(drop=True)
        
        print("Applying heuristics...")
        df = self.detect_duplicate_reviews(df)
        df = self.detect_rating_sentiment_mismatch(df)
        df = self.detect_suspicious_patterns(df)
        df = self.detect_excessive_caps(df)
        
        # Combine indicators: if 2+ indicators, mark as fake
        df['fake_score'] = (df['is_duplicate'] + df['rating_mismatch'] + 
                           df['suspicious_short'] + df['excessive_caps'] + 
                           df['has_generic'] + df['repetitive'])
        
        # Label: 1 = Fake, 0 = Real (more strict threshold)
        df['label'] = (df['fake_score'] >= 3).astype(int)
        
        fake_count = df['label'].sum()
        real_count = len(df) - fake_count
        
        print(f"\nLabel Distribution:")
        print(f"Real Reviews: {real_count} ({real_count/len(df)*100:.1f}%)")
        print(f"Fake Reviews: {fake_count} ({fake_count/len(df)*100:.1f}%)")
        
        return df
