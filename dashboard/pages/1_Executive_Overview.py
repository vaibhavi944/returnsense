import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Executive Overview", layout="wide")

st.title("📈 Business Overview")
st.info("💡 **What this page tells you:** A high-level look at how returns are affecting your total sales and the environment.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    returns_df = df[df['Return_Status'] == 'Returned']
    total_orders = len(df)
    return_rate = len(returns_df) / total_orders
    total_loss = len(returns_df) * 25
    total_co2 = len(returns_df) * 2.5

    # --- TOP ROW ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Orders", f"{total_orders:,}")
    c2.metric("Return Rate", f"{return_rate:.1%}")
    c3.metric("Money Lost", f"${total_loss:,}")
    c4.metric("CO2 Emissions", f"{total_co2:,.0f} kg")

    st.divider()

    # --- CHART SECTION ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Returns by Product Category")
        cat_data = returns_df['Product_Category'].value_counts().reset_index()
        fig = px.pie(cat_data, values='count', names='Product_Category', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Why People Return Items")
        reason_data = returns_df['Return_Reason'].value_counts().reset_index().head(5)
        fig2 = px.bar(reason_data, x='count', y='Return_Reason', orientation='h',
                      color_discrete_sequence=['#3B82F6'])
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
