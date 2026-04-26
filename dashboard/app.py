import streamlit as st
import sys
import os

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="ReturnSense Dashboard", layout="wide")

# --- DEBUG SIDEBAR ---
with st.sidebar:
    st.header("🛠️ System Debug")
    if "GROQ_API_KEY" in st.secrets:
        st.success("API Key Detected in Secrets")
        st.caption(f"Key starts with: {st.secrets['GROQ_API_KEY'][:7]}...")
    else:
        st.error("API Key NOT found in Secrets")
        st.info("Ensure it is set as GROQ_API_KEY = 'your_key' in Settings > Secrets")
    
    if st.button("♻️ Clear App Cache"):
        st.cache_resource.clear()
        st.rerun()

st.title("ReturnSense: E-commerce Return Intelligence")

# --- CLOUD SETUP: Auto-train if models are missing ---
if not os.path.exists("models/return_model.pkl"):
    st.warning("⚠️ AI Models not found. This is normal for the first launch on the cloud.")
    if st.button("🚀 Initialize AI (Train Model)"):
        with st.spinner("Training AI model on cloud... this takes about 30 seconds."):
            try:
                from src.predictor.train import train_models
                train_models()
                st.success("✅ AI Initialized successfully! You can now use the Scorer.")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"Training failed: {str(e)}")

st.markdown("""
Welcome to the **ReturnSense Dashboard**. Use the sidebar to navigate to:

- **Executive Overview:** High-level metrics on returns and financial impact.
- **Product Intelligence:** Deep dive into product return rates and reasons.
- **Seller Intelligence:** Seller performance and actionable insights.
- **Order Risk Scorer:** Predict return probability for new orders (Real-time).
- **Recommendation Engine:** Agent-generated recommendations to reduce returns.
""")
