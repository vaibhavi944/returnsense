import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Executive Overview", layout="wide")

st.title("📈 Executive Overview")
st.markdown("### High-Level Return Metrics & Financial Impact")

# Load data for real metrics
try:
    df = pd.read_csv('data/processed/classified_returns.csv')
    total_orders = len(df)
    return_rate = (df['Return_Status'] == 'Returned').mean()
    total_returns = len(df[df['Return_Status'] == 'Returned'])

    # --- ROW 1: KEY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Order Volume", f"{total_orders:,}")
    col2.metric("Average Return Rate", f"{return_rate:.2%}", "-1.2% vs Last Month")
    col3.metric("Estimated Return Loss", f"${total_returns * 25:,}", delta_color="inverse")
    col4.metric("CO2 Impact", f"{total_returns * 2.5:.1f} kg", "+5.2%")

    # --- ROW 2: VISUALS ---
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Returns by Category")
        cat_data = df[df['Return_Status'] == 'Returned']['Product_Category'].value_counts().reset_index()
        fig = px.pie(cat_data, values='count', names='Product_Category', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Return Reason Distribution")
        reason_data = df[df['Return_Status'] == 'Returned']['Return_Reason'].value_counts().reset_index()
        fig2 = px.bar(reason_data, x='count', y='Return_Reason', orientation='h',
                      color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig2, use_container_width=True)

    # --- ROW 3: SUSTAINABILITY ---
    st.success("🌱 **Sustainability Insight:** Reducing returns in the 'Clothing' category by 5% would save approximately 1,200kg of CO2 emissions this quarter.")
except Exception as e:
    st.error(f"Could not load overview data: {e}")
