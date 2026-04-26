import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Product Intelligence", layout="wide")

st.title("📦 Product Performance")
st.markdown("Check how individual products are doing. Find out which items are causing problems.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    global_avg = (df['Return_Status'] == 'Returned').mean()

    # --- SEARCH ---
    selected_prod = st.selectbox("Select a Product ID:", df['Product_ID'].unique()[:100])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    # --- SCORECARD ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Product Return Rate", f"{p_rate:.1%}")
    c2.metric("Store Average", f"{global_avg:.1%}")
    
    status = "⚠️ BAD" if p_rate > global_avg else "✅ GOOD"
    c3.subheader(f"Overall Status: {status}")

    st.divider()

    # --- VISUALS ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Why this product is returned")
        if len(returns_p) > 0:
            fig = px.bar(returns_p['Return_Reason'].value_counts().reset_index(), 
                         x='Return_Reason', y='count')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No returns recorded yet.")

    with col_b:
        st.subheader("Ages of people buying this")
        fig2 = px.histogram(p_df, x='User_Age')
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
