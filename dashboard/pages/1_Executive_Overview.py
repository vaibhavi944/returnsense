import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Executive Overview", layout="wide")

st.title("📈 Business Overview")
st.markdown("This page shows how returns are affecting your money and the environment.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    total_orders = len(df)
    returns_df = df[df['Return_Status'] == 'Returned']
    return_rate = len(returns_df) / total_orders
    total_loss = len(returns_df) * 25 # Assuming $25 loss per return
    total_co2 = len(returns_df) * 2.5 # Assuming 2.5kg CO2 per return

    # --- TOP ROW ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Orders", f"{total_orders:,}")
    m2.metric("Return Rate", f"{return_rate:.2%}")
    m3.metric("Money Lost to Returns", f"${total_loss:,}")
    m4.metric("CO2 Emissions (Pollution)", f"{total_co2:,.0f} kg")

    st.divider()

    # --- MIDDLE ROW ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Returns by Category")
        cat_data = returns_df['Product_Category'].value_counts().reset_index()
        fig = px.pie(cat_data, values='count', names='Product_Category', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Why People Return Items")
        reason_data = returns_df['Return_Reason'].value_counts().reset_index()
        fig2 = px.bar(reason_data, x='count', y='Return_Reason', orientation='h')
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
