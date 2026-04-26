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
    
    # --- MATH FIX: Calculate stats PER CITY ---
    # We want to know: How much money was actually returned in each city?
    city_stats = df.groupby('User_Location').apply(lambda x: pd.Series({
        'Return_Rate': (x['Return_Status'] == 'Returned').mean(),
        'Total_Orders': len(x),
        'Money_Lost': x[x['Return_Status'] == 'Returned']['Order_Value'].sum()
    })).reset_index()
    city_stats.columns = ['Region', 'Return_Rate', 'Total_Orders', 'Money_Lost']
    
    # --- LEADERBOARD ---
    st.subheader("Top and Bottom Regions")
    best = city_stats.sort_values('Return_Rate').head(5)
    worst = city_stats.sort_values('Return_Rate', ascending=False).head(5)
    
    c1, c2 = st.columns(2)
    with c1:
        st.success("Best Performing Regions (Low Returns)")
        st.dataframe(best[['Region', 'Return_Rate', 'Total_Orders']].style.format({'Return_Rate': '{:.1%}'}))
    with c2:
        st.error("Regions with Most Returns")
        st.dataframe(worst[['Region', 'Return_Rate', 'Total_Orders']].style.format({'Return_Rate': '{:.1%}'}))

    st.divider()

    # --- THE FIX: REAL POTENTIAL SAVINGS ---
    st.subheader("Potential Savings")
    selected_region = st.selectbox("Pick a region to audit:", city_stats['Region'].unique())
    
    # Get the specific data for THIS city only
    this_city_data = city_stats[city_stats['Region'] == selected_region].iloc[0]
    lost_amount = this_city_data['Money_Lost']
    
    # Calculate 10% of the REAL loss for this specific city
    savings = lost_amount * 0.1
    
    if savings > 0:
        st.info(f"If we reduce returns in **{selected_region}** by 10%, you could save **${savings:,.2f}** next quarter!")
        st.caption(f"(Calculated from current total loss of ${lost_amount:,.2f} in this region)")
    else:
        st.success(f"**{selected_region}** has zero return losses! No savings needed.")

except Exception as e:
    st.error(f"Error: {e}")
