import streamlit as st
import sys
import os
import importlib
from dotenv import load_dotenv

load_dotenv()

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import src.agent.agent
importlib.reload(src.agent.agent)
from src.agent.agent import generate_recommendations, get_api_key

st.set_page_config(page_title="Recommendation Engine", layout="wide")

st.title("🤖 Recommendations to Fix Returns")
st.markdown("Use this tool to get advice on how to stop returns for specific regions or products.")

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("What to Analyze")
    try:
        import pandas as pd
        df = pd.read_csv('data/processed/classified_returns.csv')
        regions = df['User_Location'].unique()[:10]
        products = df['Product_ID'].unique()[:10]
    except:
        regions = ["City5", "City11"]
        products = ["PROD01", "PROD02"]

    seller_id = st.selectbox("Pick a Region:", regions)
    product_id = st.selectbox("Pick a Product (Optional):", ["None"] + list(products))

with col2:
    st.subheader("AI Consultant Advice")
    if st.button("Get Advice", use_container_width=True):
        with st.spinner("AI is thinking..."):
            try:
                p_id = None if product_id == "None" else product_id
                data = generate_recommendations(seller_id, p_id)
                
                st.write(f"**Recommended Action Level:** {data.get('priority', 'NORMAL')}")
                
                for idx, rec in enumerate(data.get("recommendations", [])):
                    with st.expander(f"Suggestion #{idx+1}", expanded=True):
                        if isinstance(rec, dict):
                            st.write(f"**Action:** {rec.get('action', '')}")
                            st.write(rec.get('description', ''))
                        else:
                            st.write(rec)
                
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("ReturnSense v1.5")
