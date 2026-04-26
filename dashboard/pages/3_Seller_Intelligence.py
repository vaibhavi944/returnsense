import streamlit as st
import pandas as pd
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Seller Intelligence", layout="wide")

st.title("🤝 Seller Performance")
st.markdown("This page shows which regions have the most and least returns.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    seller_stats = df.groupby('User_Location').agg({
        'Return_Status': lambda x: (x == 'Returned').mean(),
        'Order_ID': 'count',
        'Order_Value': 'sum'
    }).reset_index()
    seller_stats.columns = ['Region', 'Return_Rate', 'Total_Orders', 'Total_Money']
    
    # --- LEADERBOARD ---
    st.subheader("Top and Bottom Regions")
    best = seller_stats.sort_values('Return_Rate').head(5)
    worst = seller_stats.sort_values('Return_Rate', ascending=False).head(5)
    
    c1, c2 = st.columns(2)
    with c1:
        st.success("Best Performing Regions")
        st.dataframe(best[['Region', 'Return_Rate', 'Total_Orders']])
    with c2:
        st.error("Regions with Most Returns")
        st.dataframe(worst[['Region', 'Return_Rate', 'Total_Orders']])

    st.divider()

    # --- FORECAST ---
    st.subheader("Potential Savings")
    selected_region = st.selectbox("Pick a region to audit:", seller_stats['Region'].unique())
    s_data = seller_stats[seller_stats['Region'] == selected_region].iloc[0]
    
    # Simple Math: If returns drop by 10%, how much money is saved?
    savings = s_data['Total_Money'] * s_data['Return_Rate'] * 0.1
    
    st.info(f"If we reduce returns in **{selected_region}** by 10%, you could save **${savings:,.2f}** next quarter!")

except Exception as e:
    st.error(f"Error: {e}")
