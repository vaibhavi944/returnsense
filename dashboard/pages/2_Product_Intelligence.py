import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Product Performance", layout="wide")

st.title("📦 Product Performance")
st.markdown("Check if a specific product is being returned too often.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    global_avg = (df['Return_Status'] == 'Returned').mean()

    # --- SELECTOR ---
    selected_prod = st.selectbox("Select a Product to check:", df['Product_ID'].unique()[:100])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    st.markdown("---")

    # --- STATUS CARDS (Simple & Clear) ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.metric("This Product's Return Rate", f"{p_rate:.1%}")
    with c2:
        st.metric("Store Average", f"{global_avg:.1%}")

    if p_rate > global_avg:
        st.error(f"🚨 **Warning:** {selected_prod} is being returned MORE than the average product.")
    else:
        st.success(f"✅ **Good News:** {selected_prod} is performing better than average.")

    st.divider()

    # --- SIMPLE BAR CHART ---
    st.subheader("Why people are returning this specific item")
    if len(returns_p) > 0:
        fig_bar = px.bar(returns_p['Return_Reason'].value_counts().reset_index(), 
                        x='count', y='Return_Reason', orientation='h',
                        color_discrete_sequence=['#3B82F6'])
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No returns recorded for this product yet.")

except Exception as e:
    st.error(f"Error: {e}")
