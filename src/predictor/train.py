import mlflow
import joblib
import os
import argparse
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from src.predictor.data_loader import load_data, split_data
from src.predictor.feature_builder import FeatureBuilder
from src.predictor.evaluate import evaluate_model

def train_models():
    os.makedirs('models', exist_ok=True)
    
    # Load data
    df = load_data('data/processed/classified_returns.csv')
    train_df, test_df = split_data(df)
    
    # Feature Building
    fb = FeatureBuilder()
    fb.fit(train_df)
    
    X_train = fb.transform(train_df)
    y_train = train_df['target']
    
    X_test = fb.transform(test_df)
    y_test = test_df['target']
    
    # Class imbalance weight (increased significantly to boost recall)
    pos_count = sum(y_train == 1)
    neg_count = sum(y_train == 0)
    scale_pos_weight = (neg_count / pos_count) * 4.0 if pos_count > 0 else 1.0

    # Save FeatureBuilder for inference
    joblib.dump(fb, 'models/feature_builder.pkl')
    
    # 1. Baseline Model
    print("Training Baseline Logistic Regression...")
    lr_model = LogisticRegression(class_weight='balanced', max_iter=1000)
    lr_model.fit(X_train, y_train)
    joblib.dump(lr_model, 'models/baseline_lr.pkl')
    
    # 2. XGBoost Model
    xgb_params = {
        'n_estimators': 300,
        'max_depth': 6,
        'learning_rate': 0.05,
        'scale_pos_weight': scale_pos_weight,
        'random_state': 42
    }
    
    print("Training XGBoost Model...")
    mlflow.set_experiment("ReturnSense_Modeling")
    with mlflow.start_run():
        mlflow.log_params(xgb_params)
        
        xgb_model = XGBClassifier(**xgb_params)
        xgb_model.fit(X_train, y_train)
        
        # Evaluate
        print("Evaluating Model...")
        metrics = evaluate_model(xgb_model, X_test, y_test)
        mlflow.log_metrics({
            "recall": metrics['recall'],
            "precision": metrics['precision'],
            "auc": metrics['auc']
        })
        
        joblib.dump(xgb_model, 'models/return_model.pkl')
        mlflow.xgboost.log_model(xgb_model, "xgb_model")
        print("Models trained and saved to models/ directory.")

if __name__ == '__main__':
    train_models()
