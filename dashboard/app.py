import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="ReturnSense Dashboard", layout="wide")

# --- DEBUG SIDEBAR (FIXED LOGIC) ---
with st.sidebar:
    st.header("🛠️ System Debug")
    
    # Robust multi-source key check
    has_groq = False
    
    # 1. Check Env Var (Local)
    if os.getenv("GROQ_API_KEY"):
        has_groq = True
    
    # 2. Check Streamlit Secrets (Cloud) - with crash protection
    if not has_groq:
        try:
            if "GROQ_API_KEY" in st.secrets:
                has_groq = True
        except:
            pass

    if has_groq:
        st.success("✅ Groq API Key Detected")
        st.caption("AI Agent: LLM Mode Active")
    else:
        st.error("❌ No API Key Found")
        st.info("Agent will use Fallback Rules. To fix: Add GROQ_API_KEY to your .env file or Streamlit Secrets.")
    
    st.divider()
    if st.button("♻️ Clear App Cache", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

st.title("ReturnSense: E-commerce Return Intelligence")

# --- CLOUD SETUP ---
if not os.path.exists("models/return_model.pkl"):
    st.warning("⚠️ AI Models not found.")
    if st.button("🚀 Initialize AI (Train Model)"):
        with st.spinner("Training AI model..."):
            try:
                from src.predictor.train import train_models
                train_models()
                st.success("✅ AI Initialized successfully!")
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
