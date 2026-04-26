import streamlit as st
import sys
import os
import importlib

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# --- FORCE RELOAD: Ensure the app sees the latest agent.py ---
import src.agent.agent
importlib.reload(src.agent.agent)
from src.agent.agent import generate_recommendations

st.title("Recommendation Engine")

# --- SECRET DEBUGGER ---
with st.expander("🛠️ Secret Debugger"):
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ Found 'GROQ_API_KEY' in st.secrets!")
        key = st.secrets["GROQ_API_KEY"]
        st.write(f"Key starts with: `{key[:10]}...`")
    else:
        st.error("❌ 'GROQ_API_KEY' NOT found in st.secrets")

st.info("This engine uses a Generative AI Agent to suggest business fixes.")

seller_id = st.text_input("Enter Seller ID to generate recommendations:", "SELLER001")
product_id = st.text_input("Enter Product ID (Optional):", "")

if st.button("Generate Insights"):
    with st.spinner("Agent is analyzing history and complaints..."):
        try:
            # We call the fresh version of the logic
            data = generate_recommendations(seller_id, product_id if product_id else None)
            
            source = data.get("source", "Unknown")
            version = data.get("v", "Old")
            
            st.caption(f"Engine: **{source}** | Version: **{version}**")
                
            st.subheader(f"Priority: {data['priority']}")
            for rec in data['recommendations']:
                st.info(f"💡 {rec}")
                
        except Exception as e:
            st.error(f"Error: {e}")
