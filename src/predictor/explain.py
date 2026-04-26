import shap
import pandas as pd
import joblib

class Explainer:
    def __init__(self, model_path='models/return_model.pkl', fb_path='models/feature_builder.pkl'):
        try:
            self.model = joblib.load(model_path)
            self.fb = joblib.load(fb_path)
            self.explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            print(f"Failed to load models for Explainer: {e}")
            self.model = None
            self.fb = None

    def explain_prediction(self, order_features: dict) -> dict:
        """
        Convert order features to SHAP explanation
        """
        if self.model is None or self.fb is None:
            return {"top_reasons": ["Explainability not available (Model not loaded)"]}
            
        df_raw = pd.DataFrame([order_features])
        X = self.fb.transform(df_raw)
        
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            sv = shap_values[1][0]
        else:
            sv = shap_values[0]
            
        feature_names = X.columns.tolist()
        
        contributions = sorted(zip(feature_names, sv), key=lambda x: abs(x[1]), reverse=True)
        
        top_reasons = []
        for feature, val in contributions[:3]: # Top 3 features driving the prediction
            if feature == 'product_return_rate' and val > 0:
                top_reasons.append("High product return rate")
            elif feature == 'customer_return_rate' and val > 0:
                top_reasons.append("Customer frequently returns items")
            elif feature == 'sentiment_score' and val > 0: # Usually high risk means negative sentiment, but let's just make it readable
                top_reasons.append("Negative sentiment in reviews / low confidence")
            elif feature == 'Order_Quantity' and val > 0:
                top_reasons.append("High order quantity suggests size wardrobing")
            elif val > 0:
                top_reasons.append(f"High risk associated with {feature}")
            else:
                top_reasons.append(f"Low risk associated with {feature}")
                
        return {
            "top_reasons": top_reasons
        }
