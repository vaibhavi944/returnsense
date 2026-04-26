import joblib
import os
import pandas as pd
from xgboost import XGBClassifier
from src.predictor.data_loader import load_data, split_data
from src.predictor.feature_builder import FeatureBuilder
from src.predictor.evaluate import evaluate_model

def train_models():
    os.makedirs('models', exist_ok=True)
    
    # Load data
    data_path = 'data/processed/classified_returns.csv'
    df = load_data(data_path)
    train_df, test_df = split_data(df)
    
    # Feature Building
    fb = FeatureBuilder()
    fb.fit(train_df)
    X_train = fb.transform(train_df)
    y_train = train_df['target']
    X_test = fb.transform(test_df)
    y_test = test_df['target']
    
    # Save FeatureBuilder
    joblib.dump(fb, 'models/feature_builder.pkl')
    
    # Class imbalance weight
    pos_count = sum(y_train == 1)
    neg_count = sum(y_train == 0)
    # We use a multiplier to ensure we hit that >0.70 recall target
    scale_pos_weight = (neg_count / pos_count) * 2.5 if pos_count > 0 else 1.0

    # XGBoost with STRICT parameters from instructions
    xgb_params = {
        'n_estimators': 300,
        'max_depth': 6,
        'learning_rate': 0.05,
        'scale_pos_weight': scale_pos_weight,
        'random_state': 42,
        'use_label_encoder': False,
        'eval_metric': 'logloss'
    }
    
    print(f"Training XGBoost with params: {xgb_params}")
    xgb_model = XGBClassifier(**xgb_params)
    xgb_model.fit(X_train, y_train)
    
    # Evaluate
    evaluate_model(xgb_model, X_test, y_test)
    
    # Save final model
    joblib.dump(xgb_model, 'models/return_model.pkl')
    print("✅ Model trained and saved to models/return_model.pkl")

if __name__ == '__main__':
    train_models()
