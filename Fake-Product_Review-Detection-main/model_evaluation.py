from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ModelEvaluator:
    def __init__(self):
        self.results = {}
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        y_pred = model.predict(X_test)
        
        metrics = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, average='weighted'),
            'Recall': recall_score(y_test, y_pred, average='weighted'),
            'F1-Score': f1_score(y_test, y_pred, average='weighted')
        }
        
        self.results[model_name] = metrics
        
        print(f"\n{'='*50}")
        print(f"{model_name} Results:")
        print(f"{'='*50}")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")
        print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
        
        return metrics
    
    def compare_models(self):
        df_results = pd.DataFrame(self.results).T
        print(f"\n{'='*50}")
        print("Model Comparison:")
        print(f"{'='*50}")
        print(df_results.to_string())
        
        best_model = df_results['Accuracy'].idxmax()
        best_accuracy = df_results['Accuracy'].max()
        print(f"\nBest Model: {best_model} with Accuracy: {best_accuracy:.4f}")
        
        return df_results
    
    def plot_comparison(self, df_results):
        fig, ax = plt.subplots(figsize=(10, 6))
        df_results.plot(kind='bar', ax=ax)
        plt.title('Model Performance Comparison')
        plt.ylabel('Score')
        plt.xlabel('Models')
        plt.xticks(rotation=45)
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig('model_comparison.png')
        print("\nComparison plot saved as 'model_comparison.png'")
