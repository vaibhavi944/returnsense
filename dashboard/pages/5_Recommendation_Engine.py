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

# Force reload of agent logic
import src.agent.agent
importlib.reload(src.agent.agent)
from src.agent.agent import generate_recommendations, get_api_key

st.set_page_config(page_title="Recommendation Engine", layout="wide")

st.title("🤖 Agentic Recommendation Engine")
st.markdown("---")

# --- BULLETPROOF SECRET CHECK ---
api_key = get_api_key()
has_key = True if api_key else False

with st.sidebar:
    st.header("⚙️ Configuration")
    if has_key:
        st.success("LLM Mode: Active (Groq Llama 3.1)")
    else:
        st.warning("LLM Mode: Fallback (Heuristic Rules)")
    
    st.info("The agent analyzes historical return patterns and customer feedback to generate strategic business interventions.")

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Target Entity")
    # Using real data to suggest inputs
    try:
        import pandas as pd
        df = pd.read_csv('data/processed/classified_returns.csv')
        regions = df['User_Location'].unique()[:10]
        products = df['Product_ID'].unique()[:10]
    except:
        regions = ["City5", "City11"]
        products = ["PROD0318", "PROD0169"]

    seller_id = st.selectbox("Regional Hub / Seller Region", regions, help="Select a region to analyze its return trends.")
    product_id = st.selectbox("Product ID (Optional)", ["None"] + list(products), help="Select a specific product to drill down.")
    
    st.markdown("### Contextual Constraints")
    st.multiselect("Focus Areas", ["Sizing", "Packaging", "Material Quality", "Description Accuracy"], default=["Sizing", "Description Accuracy"])

with col2:
    st.subheader("Consultant Output")
    if st.button("Generate Strategic Recommendations", use_container_width=True):
        with st.spinner("AI Agent is synthesizing historical data..."):
            try:
                # Call logic
                p_id = None if product_id == "None" else product_id
                data = generate_recommendations(seller_id, p_id)
                
                st.markdown(f"**Priority Level:** {data.get('priority', 'MEDIUM')}")
                
                for idx, rec in enumerate(data.get("recommendations", [])):
                    with st.expander(f"Recommendation #{idx+1}", expanded=True):
                        if isinstance(rec, dict):
                            st.markdown(f"### 🎯 {rec.get('action', 'Action Item')}")
                            st.write(rec.get('description', ''))
                            if 'metrics' in rec:
                                st.info(f"**Expected Impact:** {rec['metrics']}")
                        else:
                            st.write(f"💡 {rec}")
                
                st.divider()
                st.caption(f"Engine: {data.get('source', 'System')} | Intelligence Version: {data.get('v', '1.5')}")
            except Exception as e:
                st.error(f"Engine Synthesis Error: {e}")

st.markdown("---")
st.caption("ReturnSense Prescriptive Analytics Module v1.5")
