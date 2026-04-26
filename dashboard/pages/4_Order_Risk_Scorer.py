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

st.set_page_config(page_title="Order Scorer", layout="wide")

st.title("⚖️ Order Risk Scorer")
st.info("💡 **What this page tells you:** This tool uses AI to predict if a new order will be returned before you even ship it out.")

# Load real data for dropdowns
try:
    df = pd.read_csv('data/processed/classified_returns.csv')
    real_order_ids = df['Order_ID'].unique()[:50]
    real_product_ids = df['Product_ID'].unique()[:50]
    real_user_ids = df['User_ID'].unique()[:50]
    categories = df['Product_Category'].unique().tolist()
    shipping_methods = df['Shipping_Method'].unique().tolist()
    payment_methods = df['Payment_Method'].unique().tolist()
except:
    real_order_ids = ["ORD0001", "ORD0002"]
    real_product_ids = ["PROD01", "PROD02"]
    real_user_ids = ["USER01", "USER02"]
    categories = ["Clothing", "Electronics"]
    shipping_methods = ["Standard", "Express"]
    payment_methods = ["Credit Card", "PayPal"]

# --- INTERNAL AI LOGIC ---
@st.cache_resource
def load_ai_models():
    try:
        model_path = os.path.join(os.getcwd(), 'models', 'return_model.pkl')
        fb_path = os.path.join(os.getcwd(), 'models', 'feature_builder.pkl')
        if not os.path.exists(model_path): return None, None, None
        model = joblib.load(model_path)
        fb = joblib.load(fb_path)
        explainer = Explainer()
        return model, fb, explainer
    except: return None, None, None

model, fb, explainer = load_ai_models()

if model is None:
    st.error("🚨 AI Models not found! Go to the **Main Page** and click 'Initialize AI' first.")
else:
    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        with col1:
            order_id = st.selectbox("Order ID:", real_order_ids)
            product_id = st.selectbox("Product ID:", real_product_ids)
            customer_id = st.selectbox("Customer ID:", real_user_ids)
            product_category = st.selectbox("Product Category:", categories)
            user_age = st.slider("Customer Age:", 18, 80, 35)
        with col2:
            order_value = st.number_input("Order Value ($):", value=150.0)
            order_qty = st.number_input("Order Quantity:", value=1)
            shipping_method = st.selectbox("Shipping Method:", shipping_methods)
            payment_method = st.selectbox("Payment Method:", payment_methods)
            user_gender = st.selectbox("User Gender:", ["Male", "Female", "Other"])
        
        submitted = st.form_submit_button("Check Return Risk", use_container_width=True)
        
        if submitted:
            order_data = {
                "Order_ID": order_id, "Product_ID": product_id, "User_ID": customer_id,
                "Order_Value": order_value, "Order_Quantity": order_qty,
                "Product_Category": product_category, "User_Age": user_age,
                "Shipping_Method": shipping_method, "Payment_Method": payment_method,
                "User_Gender": user_gender, "Product_Price": order_value / order_qty if order_qty > 0 else 0
            }
            df_input = pd.DataFrame([order_data])
            X = fb.transform(df_input)
            prob = float(model.predict_proba(X)[0][1])
            explanation = explainer.explain_prediction(order_data)
            
            st.divider()
            st.metric("Probability of Return", f"{prob:.1%}")
            if prob > 0.7: st.error("⚠️ HIGH RISK: This order is very likely to be returned.")
            elif prob > 0.4: st.warning("⚠️ MEDIUM RISK: Be careful with this order.")
            else: st.success("✅ LOW RISK: This order is safe to ship.")
            
            st.subheader("Why this score?")
            for reason in explanation.get("top_reasons", []):
                st.write(f"🔍 {reason}")
