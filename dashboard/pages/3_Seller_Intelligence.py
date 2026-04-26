import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.set_page_config(page_title="Regional Performance", layout="wide")

st.title("🤝 Regional Performance")
st.info("💡 **What this page tells you:** Compare different cities to see where returns are highest and how much money you can save by fixing them.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    city_stats = df.groupby('User_Location').apply(lambda x: pd.Series({
        'Return_Rate': (x['Return_Status'] == 'Returned').mean(),
        'Total_Orders': int(len(x)), # Formatting as integer
        'Money_Lost': x[x['Return_Status'] == 'Returned']['Order_Value'].sum()
    })).reset_index()
    city_stats.columns = ['City', 'Return_Rate', 'Total_Orders', 'Money_Lost']
    
    # --- TOP ROW ---
    st.subheader("Best and Worst Cities")
    best = city_stats.sort_values('Return_Rate').head(5)
    worst = city_stats.sort_values('Return_Rate', ascending=False).head(5)
    
    c1, c2 = st.columns(2)
    with c1:
        st.success("Cities with Fewest Returns")
        # Fixed formatting for integers
        st.dataframe(best[['City', 'Return_Rate', 'Total_Orders']].style.format({
            'Return_Rate': '{:.1%}',
            'Total_Orders': '{:,.0f}'
        }), hide_index=True)
    with c2:
        st.error("Cities with Most Returns")
        st.dataframe(worst[['City', 'Return_Rate', 'Total_Orders']].style.format({
            'Return_Rate': '{:.1%}',
            'Total_Orders': '{:,.0f}'
        }), hide_index=True)

    st.divider()

    # --- SAVINGS SECTION ---
    st.subheader("💰 Money You Could Save")
    col_sel, col_fig = st.columns([1, 2])

    with col_sel:
        selected_city = st.selectbox("Pick a city to see savings:", city_stats['City'].unique())
        s_data = city_stats[city_stats['City'] == selected_city].iloc[0]
        
        st.markdown(f"**Current money lost in {selected_city}:** `${s_data['Money_Lost']:,.2f}`")
        reduction = st.slider("If we reduce returns by (%)", 5, 50, 15)
        savings = s_data['Money_Lost'] * (reduction/100)
        st.success(f"**You would save:** `${savings:,.2f}`")

    with col_fig:
        fig_rec = go.Figure(go.Bar(
            name='Current Loss', x=[selected_city], y=[s_data['Money_Lost']], 
            marker_color='#FEE2E2', text=f"${s_data['Money_Lost']:,.0f}"
        ))
        fig_rec.add_trace(go.Bar(
            name='Money Saved', x=[selected_city], y=[savings], 
            marker_color='#3B82F6', text=f"${savings:,.0f}"
        ))
        fig_rec.update_layout(barmode='stack', template="plotly_white", height=300)
        st.plotly_chart(fig_rec, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
