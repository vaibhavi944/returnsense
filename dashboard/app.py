import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# --- ROBUST PATH FIX (ROOT LEVEL) ---
# app.py is in dashboard/, so root is one level up (..)
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="ReturnSense Home", layout="wide")

# --- SIDEBAR DEBUG ---
with st.sidebar:
    st.header("🛠️ System Debug")
    has_groq = False
    if os.getenv("GROQ_API_KEY"): has_groq = True
    try:
        if "GROQ_API_KEY" in st.secrets: has_groq = True
    except: pass

    if has_groq:
        st.success("✅ Groq AI Active")
    else:
        st.warning("⚠️ Using Fallback Rules")
    
    st.divider()
    if st.button("♻️ Reset App Cache", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

# --- MAIN CONTENT ---
st.title("📦 Welcome to ReturnSense")
st.markdown("### The Smart Way to Stop Product Returns")

st.markdown("""
**ReturnSense** is an AI-powered system designed to help e-commerce stores reduce the number of items sent back by customers. 
By analyzing past data, our system predicts which orders are risky, explains why, and gives you real advice on how to fix the problems.
""")

st.divider()

st.markdown("### 🔍 What you can do in this dashboard:")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📈 **Business Overview**", expanded=True):
        st.write("See the 'Big Picture'. Track how much money returns are costing you and see their impact on the environment.")
    
    with st.expander("📦 **Product Performance**", expanded=True):
        st.write("Drill down into individual items. Find out which specific products are causing the most headaches and why.")

with col2:
    with st.expander("⚖️ **Order Risk Scorer**", expanded=True):
        st.write("Use our AI to check new orders. Enter order details and see the probability of a return before you ship.")

    with col2:
        with st.expander("🤝 **Regional Performance**", expanded=True):
            st.write("Compare cities and regions. See where your happiest customers are and where your logistics need work.")

st.info("💡 **Get Started:** Use the sidebar on the left to navigate to any of the pages mentioned above!")

# --- INITIALIZATION SECTION ---
if not os.path.exists(os.path.join(repo_root, "models", "return_model.pkl")):
    st.markdown("---")
    st.warning("⚠️ **First Time Setup:** The AI 'Brain' needs to be initialized to start predicting.")
    if st.button("🚀 Initialize AI (Train Model Now)", use_container_width=True):
        with st.spinner("Learning from your data... please wait 30 seconds."):
            try:
                # Ensure we are in the root directory for training paths
                os.chdir(repo_root)
                from src.predictor.train import train_models
                train_models()
                st.success("✅ AI is ready! You can now use the Scorer.")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
