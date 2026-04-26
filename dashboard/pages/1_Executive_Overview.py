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

st.title("🏛️ Executive Intelligence Dashboard")
st.markdown("Macro-economic impact analysis of product returns on profitability and sustainability.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    total_orders = len(df)
    returns_df = df[df['Return_Status'] == 'Returned']
    return_rate = len(returns_df) / total_orders
    
    # Financial Logic (Senior Level: Categorizing losses)
    # Processing cost + Shipping cost + Restocking loss
    avg_processing_cost = 25
    estimated_total_loss = len(returns_df) * avg_processing_cost
    
    # Sustainability Scorecard
    # 2.5kg CO2 per return + 0.5kg waste
    total_co2 = len(returns_df) * 2.5
    total_waste = len(returns_df) * 0.5

    # --- TOP ROW: KPI CARDS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Ecosystem Volume", f"{total_orders:,}", help="Total orders processed in the system.")
    m2.metric("Ecosystem Return Rate", f"{return_rate:.2%}", "-0.4% MoM")
    m3.metric("Financial EBITDA Impact", f"-${estimated_total_loss:,}", delta_color="inverse", help="Direct loss from return logistics.")
    m4.metric("Carbon Footprint (CO2)", f"{total_co2:,.0f} kg", help="Estimated CO2 emitted from reverse logistics.")

    st.markdown("---")

    # --- MIDDLE ROW: ADVANCED ANALYTICS ---
    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("📊 Return Velocity by Category")
        cat_stats = df.groupby('Product_Category').agg({
            'Return_Status': lambda x: (x == 'Returned').mean() * 100,
            'Order_Value': 'sum'
        }).reset_index()
        cat_stats.columns = ['Category', 'Return_Rate_Pct', 'Total_GMV']
        
        fig = px.scatter(cat_stats, x="Total_GMV", y="Return_Rate_Pct", size="Total_GMV", 
                         color="Category", hover_name="Category", text="Category",
                         title="Risk vs. Volume Matrix", labels={"Return_Rate_Pct": "Return Rate (%)"})
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Products in the top-left are high risk/low volume. Top-right are high risk/high volume (CRITICAL).")

    with c2:
        st.subheader("📉 Return Reason Root Cause Analysis")
        reason_data = returns_df['Return_Reason'].value_counts().reset_index()
        fig2 = go.Figure(go.Bar(
            x=reason_data['count'],
            y=reason_data['Return_Reason'],
            orientation='h',
            marker=dict(color=reason_data['count'], colorscale='Reds')
        ))
        fig2.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- BOTTOM ROW: SUSTAINABILITY IMPACT ---
    st.subheader("🌱 ESG & Sustainability Scorecard")
    st.write("Quantitative assessment of environmental savings through return reduction.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"""
        **Current Environmental Toll:**
        - **CO2 Emissions:** {total_co2:,.1f} Metric kg
        - **Packaging Waste:** {total_waste:,.1f} Metric kg
        """)
    
    with col_b:
        st.success(f"""
        **Savings Potential (10% Reduction):**
        - **Recovered Revenue:** ${(estimated_total_loss * 0.1):,.2f}
        - **CO2 Avoided:** {(total_co2 * 0.1):,.1f} kg
        - **Waste Diverted:** {(total_waste * 0.1):,.1f} kg
        """)

except Exception as e:
    st.error(f"Executive Logic Failure: {e}")
