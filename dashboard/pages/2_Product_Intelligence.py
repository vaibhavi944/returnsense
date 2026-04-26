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

st.set_page_config(page_title="Product Intelligence", layout="wide")

st.title("📦 Product Health & Quality Intelligence")
st.markdown("Drill-down diagnostics for product-level performance auditing.")

try:
    data_path = os.path.join(os.getcwd(), 'data', 'processed', 'classified_returns.csv')
    df = pd.read_csv(data_path)
    
    global_avg_rate = (df['Return_Status'] == 'Returned').mean()

    # --- SEARCH & FILTER ---
    st.sidebar.header("Filter Analytics")
    categories = ["All"] + df['Product_Category'].unique().tolist()
    selected_cat = st.sidebar.selectbox("Filter by Category", categories)
    
    if selected_cat != "All":
        display_df = df[df['Product_Category'] == selected_cat]
    else:
        display_df = df

    product_stats = display_df.groupby('Product_ID').agg({
        'Return_Status': lambda x: (x == 'Returned').mean(),
        'Order_Value': 'mean',
        'User_Age': 'mean'
    }).reset_index()
    product_stats.columns = ['Product_ID', 'Return_Rate', 'Avg_Price', 'Avg_Customer_Age']
    
    top_risky_products = product_stats.sort_values('Return_Rate', ascending=False)['Product_ID'].tolist()
    
    selected_prod = st.selectbox("Select Product ID for Diagnostic Audit", top_risky_products[:100])
    
    p_df = df[df['Product_ID'] == selected_prod]
    returns_p = p_df[p_df['Return_Status'] == 'Returned']
    p_rate = len(returns_p) / len(p_df) if len(p_df) > 0 else 0

    # --- ROW 1: PERFORMANCE SCORECARD ---
    st.markdown("### Performance Scorecard")
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("SKU Return Rate", f"{p_rate:.1%}")
    c2.metric("Market Benchmark", f"{global_avg_rate:.1%}")
    
    deviation = p_rate - global_avg_rate
    status_text = "CRITICAL" if deviation > 0.1 else ("WARN" if deviation > 0.05 else "STABLE")
    c3.metric("Benchmark Deviation", f"{deviation:+.1%}", delta_color="inverse")
    
    # Simple Quality Score out of 100
    quality_score = max(0, 100 - (p_rate * 200))
    c4.metric("Product Quality Score", f"{quality_score:.0f}/100")

    st.markdown("---")

    # --- ROW 2: DIAGNOSTIC VISUALS ---
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🚩 Return Reason Breakdown")
        if len(returns_p) > 0:
            reason_counts = returns_p['Return_Reason'].value_counts().reset_index()
            fig = px.pie(reason_counts, values='count', names='Return_Reason', 
                         color_discrete_sequence=px.colors.sequential.OrRd_r)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient return data for reason mapping.")

    with col_b:
        st.subheader("👥 Target Audience Audit (Age)")
        fig2 = px.histogram(p_df, x='User_Age', nbins=10, 
                            title=f"Purchase Age Distribution for {selected_prod}",
                            color='Return_Status', barmode='group',
                            color_discrete_map={'Returned': '#EF553B', 'Not Returned': '#636EFA'})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- ROW 3: STRATEGIC FORECAST ---
    st.subheader("💡 Strategic Health Assessment")
    
    if p_rate > (global_avg_rate + 0.1):
        st.error(f"""
        **Urgent Audit Required:** This SKU ({selected_prod}) is underperforming. 
        - **Primary Flaw:** {returns_p['Return_Reason'].mode()[0]}
        - **Impact:** High financial leakage.
        - **Recommendation:** Pause marketing for age group {p_df['User_Age'].mode()[0]} and inspect physical inventory for defects.
        """)
    elif p_rate < global_avg_rate:
        st.success(f"""
        **Top Performing SKU:** {selected_prod} is a benchmark for quality.
        - **Strength:** Low return rate contributes to positive EBITDA.
        - **Action:** Increase marketing spend for this product category.
        """)
    else:
        st.info(f"**Standard Performance:** {selected_prod} is tracking with global averages. Maintain existing inventory flow.")

except Exception as e:
    st.error(f"Product Diagnostic Failure: {e}")
