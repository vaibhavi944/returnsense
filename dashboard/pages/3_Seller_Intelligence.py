import streamlit as st
import sys
import os

# --- ROBUST PATH FIX ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

st.title("Seller Intelligence")

st.info("This page provides performance metrics for individual sellers.")

seller_id = st.text_input("Enter Seller ID:", "SELLER001")

if st.button("Get Seller Stats"):
    # Since we are in 'Smart Streamlit' mode, we call logic directly 
    # instead of using requests.get()
    
    # Mocking the data logic that was previously in the API
    # In a real system, this would query a database
    seller_data = {
        "seller_id": seller_id,
        "total_orders": 1500,
        "return_rate": 0.12,
        "top_returned_products": ["PROD0169", "PROD0318", "PROD0427"],
        "customer_satisfaction": "4.2/5",
        "revenue_lost_to_returns": "$24,500"
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Orders", seller_data['total_orders'])
        st.metric("Return Rate", f"{seller_data['return_rate']:.1%}")
    with col2:
        st.metric("Customer Satisfaction", seller_data['customer_satisfaction'])
        st.metric("Revenue Lost", seller_data['revenue_lost_to_returns'])

    st.subheader("⚠️ Top Returned Products")
    for prod in seller_data['top_returned_products']:
        st.write(f"- {prod}")
        
    st.success("Analysis complete. Check the 'Recommendation Engine' for specific fixes for this seller.")
