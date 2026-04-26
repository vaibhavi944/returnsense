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

st.title("📦 Product Intelligence")
st.markdown("Analyze individual product performance to identify quality flaws and sizing trends.")

try:
    df = pd.read_csv('data/processed/classified_returns.csv')
    
    # --- TOP SELECTOR ---
    selected_prod = st.selectbox("Search for a Product ID:", df['Product_ID'].unique()[:50])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df)
    avg_rate = (df['Return_Status'] == 'Returned').mean()

    # --- ROW 1: PRODUCT HEALTH CHECK ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Return Rate", f"{p_rate:.1%}")
    c2.metric("Market Benchmark", f"{avg_rate:.1%}")
    
    status = "⚠️ AT RISK" if p_rate > avg_rate else "✅ HEALTHY"
    c3.subheader(f"Status: {status}")

    st.divider()

    # --- ROW 2: DIAGNOSTICS ---
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Customer Complaint Profile")
        if len(returns_p) > 0:
            reason_counts = returns_p['Return_Reason'].value_counts().reset_index()
            fig = px.bar(reason_counts, x='Return_Reason', y='count', 
                         color='count', color_continuous_scale='Plasma')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No returns recorded for this product.")

    with col_r:
        st.subheader("Purchase Demographics (Age)")
        fig2 = px.histogram(p_df, x='User_Age', nbins=10, 
                            title="Who is buying this?", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig2, use_container_width=True)

    # --- ROW 3: AUTOMATED INSIGHT ---
    st.subheader("💡 Data-Driven Insight")
    if p_rate > 0.2:
        st.error(f"**Action Required:** {selected_prod} has a return rate significantly higher than the average. Audit the '{returns_p['Return_Reason'].iloc[0]}' reported by customers immediately.")
    else:
        st.success(f"**Optimization:** {selected_prod} is performing exceptionally well. Analyze its product description to replicate success across other products in the '{p_df['Product_Category'].iloc[0]}' category.")

except Exception as e:
    st.error(f"Error loading product intelligence: {e}")
