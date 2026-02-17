import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

nltk.download('stopwords', quiet=True)

class DataPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.tfidf = TfidfVectorizer(max_features=3000, ngram_range=(1, 3), min_df=2)
    
    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'[^a-z\s]', '', text)
        tokens = text.split()
        tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)
    
    def extract_features(self, df):
        df['cleaned_text'] = df['review_text'].apply(self.clean_text)
        df['review_length'] = df['review_text'].apply(len)
        df['word_count'] = df['review_text'].apply(lambda x: len(str(x).split()))
        df['sentiment_polarity'] = df['review_text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df['sentiment_subjectivity'] = df['review_text'].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
        df['avg_word_length'] = df['review_text'].apply(lambda x: sum(len(word) for word in str(x).split()) / max(len(str(x).split()), 1))
        df['exclamation_count'] = df['review_text'].apply(lambda x: str(x).count('!'))
        df['question_count'] = df['review_text'].apply(lambda x: str(x).count('?'))
        df['uppercase_ratio'] = df['review_text'].apply(lambda x: sum(1 for c in str(x) if c.isupper()) / max(len(str(x)), 1))
        return df
    
    def prepare_data(self, df, fit=True):
        df = self.extract_features(df)
        if fit:
            tfidf_features = self.tfidf.fit_transform(df['cleaned_text'])
        else:
            tfidf_features = self.tfidf.transform(df['cleaned_text'])
        
        additional_features = df[['review_length', 'word_count', 'sentiment_polarity', 
                                    'sentiment_subjectivity', 'avg_word_length', 'exclamation_count',
                                    'question_count', 'uppercase_ratio']].values
        from scipy.sparse import hstack
        X = hstack([tfidf_features, additional_features])
        return X, df
