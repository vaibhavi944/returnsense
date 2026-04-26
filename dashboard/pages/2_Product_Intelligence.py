import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Product Performance", layout="wide")

st.title("📦 Product Performance")
st.info("💡 **What this page tells you:** Check how specific items are doing and see exactly why people are returning them.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    global_avg = (df['Return_Status'] == 'Returned').mean()

    # --- TOP SECTION ---
    with st.container():
        col_search, _ = st.columns([1, 2])
        with col_search:
            selected_prod = st.selectbox("🔍 Pick a Product ID:", df['Product_ID'].unique()[:100])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KPI CARDS ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items Sold", f"{len(p_df)}")
    c2.metric("Items Returned", f"{len(returns_p)}")
    c3.metric("Return Rate", f"{p_rate:.1%}")
    deviation = p_rate - global_avg
    c4.metric("Vs Store Average", f"{deviation:+.1%}", delta_color="inverse")

    st.divider()

    # --- VISUALS ---
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Why customers return this item")
        if len(returns_p) > 0:
            reason_counts = returns_p['Return_Reason'].value_counts().reset_index()
            fig_reasons = px.bar(reason_counts, x='count', y='Return_Reason', 
                                 orientation='h', color_discrete_sequence=['#3B82F6'])
            fig_reasons.update_traces(width=0.5)
            st.plotly_chart(fig_reasons, use_container_width=True)
        else:
            st.info("No returns yet!")

    with col_r:
        st.subheader("Ages of people buying this")
        fig_age = px.histogram(p_df, x='User_Age', 
                               color_discrete_sequence=['#1E3A8A'],
                               template="plotly_white")
        # Add space between bars (bargap) and make bars slightly thinner
        fig_age.update_layout(bargap=0.2)
        fig_age.update_layout(xaxis_title="Customer Age", yaxis_title="Number of Buyers")
        st.plotly_chart(fig_age, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
