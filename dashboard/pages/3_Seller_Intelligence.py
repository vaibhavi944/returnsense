import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Seller Performance", layout="wide")

st.title("🤝 Seller Region Intelligence")
st.markdown("Auditing logistics and performance metrics by regional distribution hubs.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    city_stats = df.groupby('User_Location').apply(lambda x: pd.Series({
        'Return_Rate': (x['Return_Status'] == 'Returned').mean(),
        'Total_Orders': len(x),
        'Loss_Amount': x[x['Return_Status'] == 'Returned']['Order_Value'].sum()
    })).reset_index()
    city_stats.columns = ['Region', 'Return_Rate', 'Total_Orders', 'Loss_Amount']
    
    # --- ROW 1: LEADERBOARD ---
    st.subheader("🏆 Regional Reliability Index")
    best = city_stats.sort_values('Return_Rate').head(5)
    worst = city_stats.sort_values('Return_Rate', ascending=False).head(5)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Performance (Lowest Returns)**")
        st.dataframe(best.style.background_gradient(subset=['Return_Rate'], cmap='BuGn'), 
                     use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**High Risk (Highest Returns)**")
        st.dataframe(worst.style.background_gradient(subset=['Return_Rate'], cmap='Reds'), 
                     use_container_width=True, hide_index=True)

    st.divider()

    # --- ROW 2: SAVINGS FORECAST ---
    st.subheader("💰 Revenue Recovery Projection")
    col_sel, col_fig = st.columns([1, 2])

    with col_sel:
        selected_region = st.selectbox("Select Region for Optimization Forecast:", city_stats['Region'].unique())
        s_data = city_stats[city_stats['Region'] == selected_region].iloc[0]
        st.markdown(f"**Current Monthly Loss in {selected_region}:** `${s_data['Loss_Amount']:,.2f}`")
        reduction = st.slider("Target Return Reduction (%)", 5, 50, 15)
        potential_savings = s_data['Loss_Amount'] * (reduction/100)
        st.success(f"**Potential Savings:** `${potential_savings:,.2f}`")

    with col_fig:
        # Specialized chart for showing current vs potential loss
        fig_rec = go.Figure(go.Bar(
            name='Current Loss', x=[selected_region], y=[s_data['Loss_Amount']], 
            marker_color='#FEE2E2', text=f"${s_data['Loss_Amount']:,.0f}"
        ))
        fig_rec.add_trace(go.Bar(
            name='Recoverable Capital', x=[selected_region], y=[potential_savings], 
            marker_color='#4F46E5', text=f"${potential_savings:,.0f}"
        ))
        fig_rec.update_layout(barmode='stack', template="plotly_white", height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig_rec, use_container_width=True)

except Exception as e:
    st.error(f"Logic Failure: {e}")
