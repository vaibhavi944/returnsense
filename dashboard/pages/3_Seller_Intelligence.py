import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Seller Intelligence", layout="wide")

st.title("🤝 Seller Performance Intelligence")
st.markdown("Auditing third-party seller reliability and return velocity metrics.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    # Simulate Sellers using User_Location as proxy for this dataset demo
    seller_proxy = 'User_Location' 
    
    seller_stats = df.groupby(seller_proxy).agg({
        'Return_Status': lambda x: (x == 'Returned').mean(),
        'Order_ID': 'count',
        'Order_Value': 'sum'
    }).reset_index()
    seller_stats.columns = ['Seller_Region', 'Return_Rate', 'Total_Orders', 'Total_GMV']
    
    # --- TOP ROW: LEADERBOARD ---
    st.subheader("🏆 Seller Performance Leaderboard (by Region)")
    best_sellers = seller_stats.sort_values('Return_Rate').head(5)
    worst_sellers = seller_stats.sort_values('Return_Rate', ascending=False).head(5)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("Top 5 Regions (Lowest Returns)")
        st.table(best_sellers[['Seller_Region', 'Return_Rate', 'Total_Orders']])
    with col_b:
        st.error("Bottom 5 Regions (Highest Returns)")
        st.table(worst_sellers[['Seller_Region', 'Return_Rate', 'Total_Orders']])

    st.divider()

    # --- ROW 2: SELLER AUDIT ---
    selected_seller = st.selectbox("Select Regional Seller Hub for Diagnostic Audit", seller_stats['Seller_Region'].unique())
    s_data = seller_stats[seller_stats['Seller_Region'] == selected_seller].iloc[0]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Regional Return Rate", f"{s_data['Return_Rate']:.2%}")
    m2.metric("Total GMV", f"${s_data['Total_GMV']:,.0f}")
    
    avg_global = seller_stats['Return_Rate'].mean()
    m3.metric("Peer Comparison", f"{(s_data['Return_Rate'] - avg_global):+.2%}", delta_color="inverse")

    st.divider()

    # --- ROW 3: FINANCIAL RECOVERY PLAN ---
    st.subheader("💰 Revenue Recovery Forecast")
    potential_savings = s_data['Total_GMV'] * s_data['Return_Rate'] * 0.2 # Assume 20% optimization possible
    
    st.info(f"""
    **Recovery Strategy for {selected_seller}:**
    By implementing ReturnSense's AI recommendations, this seller can potentially recover **${potential_savings:,.2f}** in the next quarter.
    
    **Action Items:**
    1. Standardize quality checks at the {selected_seller} hub.
    2. Audit the top 3 high-return SKUs in this region.
    3. Update local logistics to prevent 'Damaged in Transit' returns.
    """)

except Exception as e:
    st.error(f"Seller Analytics Failure: {e}")
