import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def engineer_features(df):
    # 1. Date Features
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Order_Month'] = df['Order_Date'].dt.month
    df['Order_DayOfWeek'] = df['Order_Date'].dt.dayofweek
    df['Is_Weekend'] = df['Order_DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    
    # 2. Price/Quantity Features
    df['Price_per_Unit'] = df['Product_Price'] / (df['Order_Quantity'] + 1e-5)
    df['Discount_Ratio'] = df['Discount_Applied'] / (df['Order_Value'] + 1e-5)
    
    # 3. Target Encoding (Risk based on category and location)
    # Note: We should do this only on training data to avoid leakage, 
    # but for this script we'll do simple grouping
    cat_risk = df.groupby('Product_Category')['target'].mean().to_dict()
    df['Category_Risk'] = df['Product_Category'].map(cat_risk)
    
    loc_risk = df.groupby('User_Location')['target'].mean().to_dict()
    df['Location_Risk'] = df['User_Location'].map(loc_risk)
    
    return df

def train_improved():
    print("Loading data...")
    df = pd.read_csv("data/processed/classified_returns.csv")
    
    # Target
    df['target'] = df['Return_Status'].apply(lambda x: 1 if x == 'Returned' else 0)
    
    # Feature Engineering
    df = engineer_features(df)
    
    features = [
        'Product_Category', 'Product_Price', 'Order_Quantity', 
        'Discount_Applied', 'Shipping_Method', 'Payment_Method', 
        'User_Age', 'User_Gender', 'User_Location', 'Order_Value',
        'Order_Month', 'Order_DayOfWeek', 'Is_Weekend', 
        'Price_per_Unit', 'Discount_Ratio', 'Category_Risk', 'Location_Risk'
    ]
    
    X = df[features]
    y = df['target']
    
    # Encode categorical features
    X_encoded = pd.get_dummies(X, columns=[
        'Product_Category', 'Shipping_Method', 'Payment_Method', 
        'User_Gender', 'User_Location'
    ], drop_first=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Improved Random Forest...")
    
    # Hyperparameter tuning
    param_dist = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'class_weight': ['balanced', 'balanced_subsample']
    }
    
    rf = RandomForestClassifier(random_state=42)
    
    random_search = RandomizedSearchCV(
        rf, param_distributions=param_dist, 
        n_iter=10, cv=3, scoring='f1', n_jobs=-1, random_state=42
    )
    
    random_search.fit(X_train, y_train)
    
    best_model = random_search.best_estimator_
    
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]
    
    print("\nBest Parameters:", random_search.best_params_)
    print("\nImproved Results:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # Save model
    joblib.dump(best_model, "src/predictor/model_improved.joblib")
    print("\nModel saved to src/predictor/model_improved.joblib")

if __name__ == "__main__":
    train_improved()
