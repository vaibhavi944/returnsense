import streamlit as st
import sys
import os

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.agent.agent import generate_recommendations

st.title("Recommendation Engine")

# --- SECRET DEBUGGER (Visible only for you to fix) ---
with st.expander("🛠️ Secret Debugger (Click here if AI is not working)"):
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ Found 'GROQ_API_KEY' in st.secrets!")
        key = st.secrets["GROQ_API_KEY"]
        st.write(f"Key starts with: `{key[:10]}...`")
        st.write(f"Total length of key: {len(key)} characters")
    else:
        st.error("❌ 'GROQ_API_KEY' NOT found in st.secrets")
        st.info("Found these keys instead: " + str(list(st.secrets.keys())))
        st.markdown("""
        **How to fix:**
        1. Go to your Streamlit Cloud Dashboard.
        2. Settings -> Secrets.
        3. Paste this EXACTLY:
        ```toml
        GROQ_API_KEY = "gsk_..."
        ```
        4. Make sure there are no spaces around `GROQ_API_KEY`.
        """)

st.info("This engine uses a Generative AI Agent to suggest business fixes.")

seller_id = st.text_input("Enter Seller ID to generate recommendations:", "SELLER001")
product_id = st.text_input("Enter Product ID (Optional):", "")

if st.button("Generate Insights"):
    with st.spinner("Agent is analyzing history and complaints..."):
        try:
            data = generate_recommendations(seller_id, product_id if product_id else None)
            
            # Show version and source
            source = data.get("source", "Unknown Version")
            version = data.get("v", "Old")
            
            st.caption(f"Engine: **{source}** | App Version: **{version}**")
                
            st.subheader(f"Priority: {data['priority']}")
            for rec in data['recommendations']:
                st.info(f"💡 {rec}")
                
        except Exception as e:
            st.error(f"Error: {e}")
