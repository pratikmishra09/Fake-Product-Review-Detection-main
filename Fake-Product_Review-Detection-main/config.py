import os

class Config:
    # Model settings
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/svm.pkl')
    SAMPLE_SIZE = int(os.getenv('SAMPLE_SIZE', 50000))
    
    # API settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Feature extraction
    MAX_FEATURES = int(os.getenv('MAX_FEATURES', 3000))
    NGRAM_RANGE = (1, 3)
    
    # Model hyperparameters
    SVM_C = float(os.getenv('SVM_C', 10))
    SVM_KERNEL = os.getenv('SVM_KERNEL', 'rbf')
    RF_ESTIMATORS = int(os.getenv('RF_ESTIMATORS', 200))
    
    # Label generation
    FAKE_THRESHOLD = int(os.getenv('FAKE_THRESHOLD', 3))
