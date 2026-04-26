import streamlit as st
import sys
import os

# --- PATH FIX ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agent.agent import generate_recommendations

st.title("Recommendation Engine")

st.info("This engine uses a Generative AI Agent to suggest business fixes.")

seller_id = st.text_input("Enter Seller ID to generate recommendations:", "SELLER001")
product_id = st.text_input("Enter Product ID (Optional):", "")

if st.button("Generate Insights"):
    with st.spinner("Agent is analyzing history and complaints..."):
        try:
            data = generate_recommendations(seller_id, product_id if product_id else None)
            st.subheader(f"Priority: {data['priority']}")
            for rec in data['recommendations']:
                st.info(f"💡 {rec}")
        except Exception as e:
            st.error(f"Error generating insights: {e}")
