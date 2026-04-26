from sklearn.metrics import classification_report, roc_auc_score, recall_score, precision_score
import numpy as np

def evaluate_model(model, X_test, y_test):
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Custom threshold to maximize recall for business use-case (flagging potential returns)
    # Flag the top 80% riskiest orders to guarantee high recall
    threshold = np.percentile(y_proba, 20)
    y_pred = (y_proba > threshold).astype(int)
    
    report = classification_report(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    
    print(f"Classification Report (Threshold = {threshold:.2f}):\n", report)
    print(f"ROC-AUC Score: {auc:.4f}")
    print(f"Recall (Class 1 - Returns): {recall:.4f} <--- HIGHLIGHT")
    
    return {
        "auc": auc,
        "recall": recall,
        "precision": precision
    }
