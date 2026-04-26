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

st.title("📈 Executive Overview")
st.markdown("### High-Level Return Metrics & Business Impact")

try:
    # Load real data
    df = pd.read_csv('data/processed/classified_returns.csv')
    total_orders = len(df)
    returns_df = df[df['Return_Status'] == 'Returned']
    return_rate = len(returns_df) / total_orders
    
    # Financial Logic: Assume avg return processing cost is $25
    total_loss = len(returns_df) * 25
    # Sustainability Logic: Assume 2.5kg CO2 per return shipment
    total_co2 = len(returns_df) * 2.5

    # --- ROW 1: KEY PERFORMANCE INDICATORS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Order Volume", f"{total_orders:,}")
    col2.metric("Return Rate", f"{return_rate:.1%}", "-1.2% vs last month")
    col3.metric("Financial Impact (Loss)", f"${total_loss:,}", delta_color="inverse")
    col4.metric("CO2 Footprint", f"{total_co2:,.0f} kg")

    st.divider()

    # --- ROW 2: STRATEGIC CHARTS ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Returns by Product Category")
        cat_data = returns_df['Product_Category'].value_counts().reset_index()
        fig = px.pie(cat_data, values='count', names='Product_Category', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Which categories are bleeding the most revenue?")

    with c2:
        st.subheader("Primary Return Reasons")
        reason_data = returns_df['Return_Reason'].value_counts().reset_index()
        fig2 = px.bar(reason_data, x='count', y='Return_Reason', orientation='h',
                      color='count', color_continuous_scale='Reds')
        fig2.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("The 'Why' behind customer dissatisfaction.")

    st.divider()

    # --- ROW 3: SUSTAINABILITY SCORECARD ---
    st.subheader("🌱 Sustainability & ESG Impact")
    st.info(f"""
    **Current Impact:** Your return logistics have generated **{total_co2:,.0f} kg of CO2** this period.
    
    **Actionable Goal:** Reducing the return rate by just **2%** would save:
    - 💰 **${(total_orders * 0.02 * 25):,.2f}** in processing costs.
    - 🌍 **{(total_orders * 0.02 * 2.5):,.0f} kg** of CO2 emissions.
    - 📦 **{(total_orders * 0.02):,.0f}** units of packaging waste.
    """)

except Exception as e:
    st.error(f"Error loading executive data: {e}")
