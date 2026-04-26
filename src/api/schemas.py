from pydantic import BaseModel
from typing import Optional, List

class OrderPredictRequest(BaseModel):
    order_id: str
    product_id: str
    customer_id: str
    order_value: float
    order_quantity: Optional[int] = 1
    product_price: Optional[float] = 0.0
    discount_applied: Optional[float] = 0.0
    user_age: Optional[int] = 30
    shipping_method: Optional[str] = "Standard"
    payment_method: Optional[str] = "Credit Card"
    user_gender: Optional[str] = "Other"
    product_category: Optional[str] = "Other"
    
class PredictResponse(BaseModel):
    return_probability: float
    risk_level: str
    top_reasons: List[str]
    
class ClassifyRequest(BaseModel):
    return_reason: str

class ClassifyResponse(BaseModel):
    category: str
    confidence: float

class RecommendationRequest(BaseModel):
    seller_id: str
