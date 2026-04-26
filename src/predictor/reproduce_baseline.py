import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

def train_baseline():
    print("Loading data...")
    df = pd.read_csv("data/processed/classified_returns.csv")
    
    # Preprocessing as in notebook
    df['target'] = df['Return_Status'].apply(lambda x: 1 if x == 'Returned' else 0)
    
    features = [
        'Product_Category',
        'Product_Price',
        'Order_Quantity',
        'Discount_Applied',
        'Shipping_Method',
        'Payment_Method',
        'User_Age',
        'User_Gender',
        'User_Location',
        'Order_Value',
        'category'
    ]
    
    X = df[features]
    y = df['target']
    
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )
    
    print("Training XGBoost baseline...")
    # Calculate scale_pos_weight
    ratio = float(y_train.value_counts()[0]) / y_train.value_counts()[1]
    
    model = XGBClassifier(scale_pos_weight=ratio, eval_metric='logloss')
    model.fit(X_train, y_train)
    
    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob > 0.3).astype(int)
    
    print("\nBaseline Results:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

if __name__ == "__main__":
    train_baseline()
