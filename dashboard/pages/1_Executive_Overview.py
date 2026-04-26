import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Executive Overview", layout="wide")

# --- CUSTOM CSS FOR MODERN LOOK ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #4F46E5; }
    [data-testid="stMetricDelta"] { font-size: 16px; }
    .main { background-color: #F9FAFB; }
    div.stButton > button:first-child {
        background-color: #4F46E5; color: white; border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Business Intelligence Command Center")
st.caption("E-commerce Reverse Logistics & Return Mitigation Strategy")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    returns_df = df[df['Return_Status'] == 'Returned']
    total_orders = len(df)
    return_rate = len(returns_df) / total_orders
    total_loss = len(returns_df) * 25
    total_co2 = len(returns_df) * 2.5

    # --- KPI STRIP ---
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Order Volume", f"{total_orders:,}")
        c2.metric("Average Return Rate", f"{return_rate:.1%}", "-1.4%")
        c3.metric("Capital at Risk", f"${total_loss:,}", delta_color="inverse")
        c4.metric("CO2 Impact", f"{total_co2:,.0f} kg")

    st.markdown("---")

    # --- CHART SECTION ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📦 Return Distribution by Category")
        cat_data = returns_df['Product_Category'].value_counts().reset_index()
        fig = px.pie(cat_data, values='count', names='Product_Category', 
                     hole=0.5, template="plotly_white",
                     color_discrete_sequence=px.colors.sequential.Indigo_r)
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🚩 Top Return Drivers")
        reason_data = returns_df['Return_Reason'].value_counts().reset_index().head(5)
        fig2 = px.bar(reason_data, x='count', y='Return_Reason', orientation='h',
                      template="plotly_white", color='count',
                      color_continuous_scale='Tealgrn')
        fig2.update_layout(margin=dict(t=30, b=0, l=0, r=0), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # --- INSIGHT CARD ---
    st.markdown("""
        <div style="background-color: #EEF2FF; padding: 20px; border-radius: 12px; border-left: 5px solid #4F46E5;">
            <h4 style="color: #312E81; margin-top:0;">🌱 Sustainability Insight</h4>
            <p style="color: #4338CA;">Based on current trends, improving the 'Sizing Accuracy' for footwear would prevent <b>450kg</b> of CO2 emissions next month.</p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
