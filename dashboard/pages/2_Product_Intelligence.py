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

st.title("📦 Product Performance Diagnostic")
st.markdown("Detailed audit of individual SKUs to identify quality trends and customer friction points.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    global_avg = (df['Return_Status'] == 'Returned').mean()

    # --- TOP SECTION: SELECTOR ---
    with st.container():
        col_search, _ = st.columns([1, 2])
        with col_search:
            selected_prod = st.selectbox("🔍 Search Product ID:", df['Product_ID'].unique()[:100])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MIDDLE SECTION: KPI CARDS ---
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Units Sold", f"{len(p_df)}")
        c2.metric("Total Returns", f"{len(returns_p)}")
        c3.metric("Return Rate", f"{p_rate:.1%}")
        
        # Deviation from store average
        deviation = p_rate - global_avg
        c4.metric("Vs Store Average", f"{deviation:+.1%}", delta_color="inverse")

    st.divider()

    # --- BOTTOM SECTION: VISUALS ---
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("🚩 Top Return Drivers")
        if len(returns_p) > 0:
            # Clean horizontal bar chart
            reason_counts = returns_p['Return_Reason'].value_counts().reset_index()
            fig_reasons = px.bar(reason_counts, x='count', y='Return_Reason', 
                                 orientation='h', template="plotly_white",
                                 color='count', color_continuous_scale='Blues')
            fig_reasons.update_layout(showlegend=False, coloraxis_showscale=False, 
                                      margin=dict(l=0, r=0, t=20, b=0), height=300)
            fig_reasons.update_traces(width=0.5) # Sleek bars
            st.plotly_chart(fig_reasons, use_container_width=True)
        else:
            st.info("No returns recorded for this SKU yet.")

    with col_r:
        st.subheader("👥 Buyer Age Distribution")
        # Histogram with professional styling
        fig_age = px.histogram(p_df, x='User_Age', nbins=10, 
                               template="plotly_white",
                               color_discrete_sequence=['#1E3A8A'])
        fig_age.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=300,
                              xaxis_title="Customer Age", yaxis_title="Number of Buyers")
        st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- FINAL SECTION: STRATEGIC INSIGHT ---
    st.subheader("💡 Strategic Health Assessment")
    with st.container():
        if p_rate > (global_avg + 0.05):
            st.error(f"""
            **Critical Alert:** {selected_prod} is underperforming. 
            - **Primary Issue:** The leading reason for returns is **{returns_p['Return_Reason'].mode()[0]}**.
            - **Action Item:** Audit the product listing for accuracy and check batch quality.
            """)
        elif p_rate < (global_avg - 0.05):
            st.success(f"""
            **High-Performing SKU:** {selected_prod} is a store benchmark. 
            - **Status:** Return rate is significantly lower than average.
            - **Action Item:** Consider increasing inventory or featuring this item in marketing campaigns.
            """)
        else:
            st.info(f"**Stable Performance:** {selected_prod} is tracking within normal parameters.")

except Exception as e:
    st.error(f"Logic Failure: {e}")
