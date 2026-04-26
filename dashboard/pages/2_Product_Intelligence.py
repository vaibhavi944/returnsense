import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Product Intelligence", layout="wide")

st.title("📦 Product Performance Audit")
st.markdown("Detailed health metrics for individual Stock Keeping Units (SKUs)")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    global_avg = (df['Return_Status'] == 'Returned').mean()

    # --- SEARCH ---
    selected_prod = st.selectbox("Select a Product to Audit:", df['Product_ID'].unique()[:50])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TOP ROW: GAUGE & METRICS ---
    col_gauge, col_info = st.columns([1, 2])

    with col_gauge:
        # Professional Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_rate * 100,
            title = {'text': "Risk Level (%)"},
            gauge = {
                'axis': {'range': [0, 50]},
                'bar': {'color': "#4F46E5"},
                'steps': [
                    {'range': [0, global_avg*100], 'color': "#E0E7FF"},
                    {'range': [global_avg*100, 50], 'color': "#FEE2E2"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': global_avg * 100
                }
            }
        ))
        fig_gauge.update_layout(margin=dict(t=0, b=0, l=20, r=20), height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_info:
        st.markdown(f"### Performance Summary for {selected_prod}")
        st.write(f"This product is tracking at a **{p_rate:.1%}** return rate compared to the store average of **{global_avg:.1%}**.")
        
        if p_rate > global_avg:
            st.error(f"⚠️ **Action Required:** Return rate is {(p_rate - global_avg):.1%} above benchmark.")
        else:
            st.success("✅ **Healthy SKU:** This product is performing better than the average.")

    st.divider()

    # --- SECOND ROW: VISUALS ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🚩 Feedback Root Cause")
        if len(returns_p) > 0:
            fig_bar = px.bar(returns_p['Return_Reason'].value_counts().reset_index(), 
                            x='count', y='Return_Reason', orientation='h',
                            template="plotly_white", color_discrete_sequence=['#4F46E5'])
            fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No returns recorded for this SKU.")

    with c2:
        st.subheader("👥 Target Audience Audit")
        fig_hist = px.histogram(p_df, x='User_Age', nbins=10, 
                               template="plotly_white", color_discrete_sequence=['#0D9488'])
        fig_hist.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_hist, use_container_width=True)

except Exception as e:
    st.error(f"Logic Error: {e}")
