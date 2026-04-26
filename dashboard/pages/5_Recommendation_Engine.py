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
from src.agent.agent import generate_recommendations

st.set_page_config(page_title="Recommendation Engine", layout="wide")

st.title("🤖 Agentic Recommendation Engine")
st.markdown("---")

# --- SAFE SECRET CHECK ---
has_key = False
try:
    if "GROQ_API_KEY" in st.secrets:
        has_key = True
except Exception:
    if os.getenv("GROQ_API_KEY"):
        has_key = True

with st.sidebar:
    st.header("⚙️ Configuration")
    if has_key:
        st.success("LLM Mode: Active (Groq Llama 3.1)")
    else:
        st.warning("LLM Mode: Fallback (Heuristic Rules)")
    
    st.info("The agent analyzes historical return patterns and unstructured customer feedback to generate strategic interventions.")

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Target Entity")
    seller_id = st.text_input("Seller ID", "SELLER_ALPHA", help="Enter the unique identifier for the seller.")
    product_id = st.text_input("Product ID (Optional)", "", help="Enter a specific product to drill down into its issues.")
    
    st.markdown("### Contextual Constraints")
    priority_filter = st.multiselect("Focus Areas", ["Sizing", "Packaging", "Material Quality", "Description Accuracy"], default=["Sizing", "Description Accuracy"])

with col2:
    st.subheader("Consultant Output")
    if st.button("Generate Strategic Recommendations", use_container_width=True):
        with st.spinner("AI Agent is synthesizing historical data..."):
            try:
                data = generate_recommendations(seller_id, product_id if product_id else None)
                
                # Professional Display
                st.markdown(f"**Priority Level:** {data.get('priority', 'MEDIUM')}")
                
                for idx, rec in enumerate(data.get("recommendations", [])):
                    with st.expander(f"Recommendation #{idx+1}", expanded=True):
                        st.write(f"💡 {rec}")
                
                st.caption(f"Engine: {data.get('source', 'System')} | Intelligence Version: {data.get('v', '1.0')}")
            except Exception as e:
                st.error(f"Engine Synthesis Error: {e}")

st.markdown("---")
st.caption("ReturnSense Prescriptive Analytics Module v1.5")
