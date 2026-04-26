from fastapi import APIRouter, HTTPException
from src.api.schemas import OrderPredictRequest, PredictResponse, ClassifyRequest, ClassifyResponse
import joblib
import pandas as pd
from src.predictor.explain import Explainer
from src.agent.agent import generate_recommendations

router = APIRouter()

# Try to load models on startup
try:
    model = joblib.load('models/return_model.pkl')
    fb = joblib.load('models/feature_builder.pkl')
    explainer = Explainer()
except Exception as e:
    model = None
    fb = None
    explainer = None
    print(f"Warning: Models not loaded. {e}")

@router.post("/predict-return-risk", response_model=PredictResponse)
async def predict_return_risk(request: OrderPredictRequest):
    if model is None or fb is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Train the model first.")
        
    order_data = {
        "Order_ID": request.order_id,
        "Product_ID": request.product_id,
        "User_ID": request.customer_id,
        "Order_Value": request.order_value,
        "Order_Quantity": request.order_quantity,
        "Product_Price": request.product_price,
        "Discount_Applied": request.discount_applied,
        "User_Age": request.user_age,
        "Shipping_Method": request.shipping_method,
        "Payment_Method": request.payment_method,
        "User_Gender": request.user_gender,
        "Product_Category": request.product_category
    }
    
    # Predict
    df = pd.DataFrame([order_data])
    X = fb.transform(df)
    prob = float(model.predict_proba(X)[0][1])
    
    risk_level = "HIGH" if prob > 0.7 else ("MEDIUM" if prob > 0.4 else "LOW")
    
    # Explain
    explanation = explainer.explain_prediction(order_data)
    
    return PredictResponse(
        return_probability=prob,
        risk_level=risk_level,
        top_reasons=explanation.get("top_reasons", [])
    )

@router.post("/classify-return", response_model=ClassifyResponse)
async def classify_return(request: ClassifyRequest):
    text = request.return_reason.lower()
    if "size" in text or "fit" in text or "small" in text or "large" in text:
        return ClassifyResponse(category="Size Issue", confidence=0.92)
    elif "damage" in text or "broken" in text or "defective" in text:
        return ClassifyResponse(category="Damaged", confidence=0.88)
    else:
        return ClassifyResponse(category="Other", confidence=0.75)

@router.get("/seller-intelligence/{seller_id}")
async def seller_intelligence(seller_id: str):
    return {
        "seller_id": seller_id,
        "total_orders": 1500,
        "return_rate": 0.12,
        "top_returned_products": ["PROD01", "PROD05"]
    }

@router.post("/generate-recommendations")
async def get_recommendations(seller_id: str, product_id: str = None):
    return generate_recommendations(seller_id, product_id)
