from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib
import os

class ModelTrainer:
    def __init__(self):
        self.models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0, random_state=42, solver='liblinear'),
            'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=5, random_state=42),
            'SVM': SVC(kernel='rbf', C=10, gamma='scale', random_state=42, probability=True)
        }
        self.trained_models = {}
    
    def train_all(self, X_train, y_train):
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            self.trained_models[name] = model
        return self.trained_models
    
    def save_models(self, path='models'):
        os.makedirs(path, exist_ok=True)
        for name, model in self.trained_models.items():
            filename = f"{path}/{name.replace(' ', '_').lower()}.pkl"
            joblib.dump(model, filename)
            print(f"Saved {name} to {filename}")
