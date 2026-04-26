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
    # Use absolute path to ensure data loads correctly
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    # Pre-calculate global average return rate (The Benchmark)
    global_avg_rate = (df['Return_Status'] == 'Returned').mean()

    # --- TOP SELECTOR ---
    # Sort products by return rate to make the dropdown more interesting
    product_stats = df.groupby('Product_ID')['Return_Status'].apply(lambda x: (x == 'Returned').mean()).reset_index()
    product_stats.columns = ['Product_ID', 'Return_Rate']
    top_products = product_stats.sort_values('Return_Rate', ascending=False)['Product_ID'].tolist()
    
    selected_prod = st.selectbox("Search for a Product ID:", top_products[:100])
    
    # Filter for the specific product
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    
    # Specific Product Return Rate
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    # --- ROW 1: PRODUCT HEALTH CHECK ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Product Return Rate", f"{p_rate:.1%}")
    c2.metric("Market Benchmark", f"{global_avg_rate:.1%}")
    
    # Compare product to market
    delta = p_rate - global_avg_rate
    if delta > 0.05:
        status = "⚠️ AT RISK (High Returns)"
        st_color = "error"
    elif delta < -0.05:
        status = "✅ HEALTHY (Low Returns)"
        st_color = "success"
    else:
        status = "⚖️ NEUTRAL (Average)"
        st_color = "info"
        
    c3.subheader(f"Status: {status}")

    st.divider()

    # --- ROW 2: DIAGNOSTICS ---
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Customer Complaint Profile")
        if len(returns_p) > 0:
            reason_counts = returns_p['Return_Reason'].value_counts().reset_index()
            fig = px.bar(reason_counts, x='Return_Reason', y='count', 
                         color='count', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No returns recorded for this specific product.")

    with col_r:
        st.subheader("Purchase Demographics (Age)")
        fig2 = px.histogram(p_df, x='User_Age', nbins=10, 
                            title=f"Who is buying {selected_prod}?", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig2, use_container_width=True)

    # --- ROW 3: AUTOMATED INSIGHT ---
    st.subheader("💡 Data-Driven Insight")
    if p_rate > (global_avg_rate + 0.1):
        st.error(f"**Critical Insight:** {selected_prod} is being returned at a rate significantly higher than your store average. Most customers mention '{returns_p['Return_Reason'].mode()[0]}' as the issue.")
    elif p_rate < global_avg_rate:
        st.success(f"**Best Practice:** {selected_prod} is a top performer. Its return rate is better than the market benchmark.")
    else:
        st.info(f"**Performance:** {selected_prod} is aligned with your store's average performance metrics.")

except Exception as e:
    st.error(f"Error loading product intelligence: {e}")
