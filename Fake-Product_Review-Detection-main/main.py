import pandas as pd
from sklearn.model_selection import train_test_split
from label_generator import SyntheticLabelGenerator
from data_preprocessing import DataPreprocessor
from model_training import ModelTrainer
from model_evaluation import ModelEvaluator
import warnings
warnings.filterwarnings('ignore')

def main():
    print("="*60)
    print("FAKE PRODUCT REVIEW DETECTION SYSTEM")
    print("="*60)
    
    # Load dataset
    print("\n[1/6] Loading dataset...")
    df = pd.read_csv('ecommerce_product_reviews_dataset.csv')
    print(f"Dataset loaded: {df.shape[0]} reviews")
    
    # Generate synthetic labels
    print("\n[2/6] Generating synthetic fake/real labels...")
    label_gen = SyntheticLabelGenerator()
    df = label_gen.generate_labels(df, sample_size=50000)
    
    # Preprocess data
    print("\n[3/6] Preprocessing data...")
    preprocessor = DataPreprocessor()
    X, df_processed = preprocessor.prepare_data(df, fit=True)
    y = df_processed['label']
    print(f"Features extracted: {X.shape[1]} features")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
    
    # Train models
    print("\n[4/6] Training models...")
    trainer = ModelTrainer()
    trained_models = trainer.train_all(X_train, y_train)
    
    # Evaluate models
    print("\n[5/6] Evaluating models...")
    evaluator = ModelEvaluator()
    for name, model in trained_models.items():
        evaluator.evaluate_model(model, X_test, y_test, name)
    
    # Compare results
    print("\n[6/6] Comparing models...")
    df_results = evaluator.compare_models()
    evaluator.plot_comparison(df_results)
    
    # Save models
    trainer.save_models()
    
    # Save preprocessor
    import joblib
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    print("Saved preprocessor to models/preprocessor.pkl")
    
    print("\n" + "="*60)
    print("PROCESS COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    main()
