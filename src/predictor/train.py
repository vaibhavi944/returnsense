import joblib
import os
import argparse
import pandas as pd
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression

# Use absolute imports to be safe
from src.predictor.data_loader import load_data, split_data
from src.predictor.feature_builder import FeatureBuilder
from src.predictor.evaluate import evaluate_model

def train_models():
    # 1. Create directory
    os.makedirs('models', exist_ok=True)
    
    # 2. Load data
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
        
    df = load_data(data_path)
    train_df, test_df = split_data(df)
    
    # 3. Feature Building
    fb = FeatureBuilder()
    fb.fit(train_df)
    
    X_train = fb.transform(train_df)
    y_train = train_df['target']
    
    X_test = fb.transform(test_df)
    y_test = test_df['target']
    
    # Save FeatureBuilder
    joblib.dump(fb, 'models/feature_builder.pkl')
    
    # 4. XGBoost Model
    pos_count = sum(y_train == 1)
    neg_count = sum(y_train == 0)
    scale_pos_weight = (neg_count / pos_count) * 4.0 if pos_count > 0 else 1.0

    xgb_params = {
        'n_estimators': 100, # Faster training for cloud
        'max_depth': 4,
        'learning_rate': 0.1,
        'scale_pos_weight': scale_pos_weight,
        'random_state': 42
    }
    
    xgb_model = XGBClassifier(**xgb_params)
    xgb_model.fit(X_train, y_train)
    
    # 5. Evaluate and Save
    evaluate_model(xgb_model, X_test, y_test)
    joblib.dump(xgb_model, 'models/return_model.pkl')
    
    # MLflow is optional - if it fails, we don't care on the cloud
    try:
        import mlflow
        mlflow.set_experiment("ReturnSense_Cloud")
        with mlflow.start_run():
            mlflow.log_params(xgb_params)
            mlflow.xgboost.log_model(xgb_model, "xgb_model")
    except Exception:
        pass 

if __name__ == '__main__':
    train_models()
