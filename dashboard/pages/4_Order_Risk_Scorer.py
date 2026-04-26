import streamlit as st
import pandas as pd
import joblib
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.predictor.explain import Explainer

st.title("Order Risk Scorer")

# --- INTERNAL AI LOGIC ---
@st.cache_resource
def load_ai_models():
    try:
        model_path = os.path.join(os.getcwd(), 'models', 'return_model.pkl')
        fb_path = os.path.join(os.getcwd(), 'models', 'feature_builder.pkl')
        
        if not os.path.exists(model_path):
            return None, None, None
            
        model = joblib.load(model_path)
        fb = joblib.load(fb_path)
        explainer = Explainer()
        return model, fb, explainer
    except Exception as e:
        st.sidebar.error(f"Model load error: {e}")
        return None, None, None

model, fb, explainer = load_ai_models()

if model is None:
    st.error("🚨 AI Models not found! Go to the **Main Page** and click 'Initialize AI' first.")
else:
    st.info("""
    **Tip:** Use IDs from the dataset to see real historical risk. 
    - **High Risk Product:** `PROD0318` 
    - **High Risk Customer:** `USER1469`
    """)

    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            order_id = st.text_input("Order ID", "ORD9999")
            product_id = st.text_input("Product ID (Try: PROD0318)", "PROD0318")
            customer_id = st.text_input("Customer ID (Try: USER1469)", "USER1469")
            product_category = st.selectbox("Product Category", ["Clothing", "Electronics", "Home", "Toys", "Books"])
            user_age = st.slider("Customer Age", 18, 80, 35)

        with col2:
            order_value = st.number_input("Order Value ($)", value=150.0)
            order_qty = st.number_input("Order Quantity", value=1)
            shipping_method = st.selectbox("Shipping Method", ["Standard", "Express", "Next-Day"])
            payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "COD", "Wallet"])
            user_gender = st.selectbox("User Gender", ["Male", "Female", "Other"])
        
        submitted = st.form_submit_button("Predict Risk")
        
        if submitted:
            order_data = {
                "Order_ID": order_id, "Product_ID": product_id, "User_ID": customer_id,
                "Order_Value": order_value, "Order_Quantity": order_qty,
                "Product_Category": product_category, "User_Age": user_age,
                "Shipping_Method": shipping_method, "Payment_Method": payment_method,
                "User_Gender": user_gender, "Product_Price": order_value / order_qty if order_qty > 0 else 0
            }
            
            df = pd.DataFrame([order_data])
            X = fb.transform(df)
            prob = float(model.predict_proba(X)[0][1])
            explanation = explainer.explain_prediction(order_data)
            
            st.metric("Return Probability", f"{prob:.1%}")
            risk_level = "HIGH" if prob > 0.7 else ("MEDIUM" if prob > 0.4 else "LOW")
            if prob > 0.7:
                st.error(f"RISK LEVEL: {risk_level}")
            elif prob > 0.4:
                st.warning(f"RISK LEVEL: {risk_level}")
            else:
                st.success(f"RISK LEVEL: {risk_level}")
            
            st.subheader("Why this score?")
            for reason in explanation.get("top_reasons", []):
                st.write(f"🔍 {reason}")
