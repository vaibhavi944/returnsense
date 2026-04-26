import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Product Intelligence", layout="wide")

st.title("📦 Product Intelligence")
st.markdown("Detailed analysis of product-level return performance and customer feedback.")

try:
    df = pd.read_csv('data/processed/classified_returns.csv')

    # --- SELECTOR ---
    target_product = st.selectbox("Select a Product to Analyze:", df['Product_ID'].unique()[:20])

    p_df = df[df['Product_ID'] == target_product]
    p_return_rate = (p_df['Return_Status'] == 'Returned').mean()
    avg_rate = (df['Return_Status'] == 'Returned').mean()

    # --- METRICS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Product Return Rate", f"{p_return_rate:.1%}")
    c2.metric("Category Avg", f"{avg_rate:.1%}")
    status = "⚠️ ABOVE AVG" if p_return_rate > avg_rate else "✅ BELOW AVG"
    c3.info(f"Status: {status}")

    # --- ANALYSIS ---
    st.divider()
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Return Reasons for this Product")
        returns_subset = p_df[p_df['Return_Status'] == 'Returned']
        if len(returns_subset) > 0:
            fig = px.bar(returns_subset['Return_Reason'].value_counts().reset_index(),
                         x='Return_Reason', y='count', color='count', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No returns recorded for this product yet.")

    with col_right:
        st.subheader("Customer Demographics")
        fig2 = px.histogram(p_df, x='User_Age', nbins=10, title="Age Distribution of Buyers", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig2, use_container_width=True)

    # --- RECOMMENDATION ---
    st.subheader("🛠️ Strategic Recommendation")
    if p_return_rate > 0.2:
        st.error(f"High risk detected for {target_product}. Immediate action required: Audit product description and sizing charts.")
    else:
        st.success(f"{target_product} is performing well. Consider using its description style as a template for other products.")
except Exception as e:
    st.error(f"Could not load product data: {e}")
