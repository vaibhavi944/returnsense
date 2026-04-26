import streamlit as st
import requests
import os

st.title("Seller Intelligence")

seller_id = st.text_input("Enter Seller ID:", "SELLER001")

if st.button("Get Seller Stats"):
    try:
        res = requests.get(f"{os.getenv('API_URL', 'http://localhost:8000')}/seller-intelligence/{seller_id}")
        if res.status_code == 200:
            data = res.json()
            st.metric("Total Orders", data['total_orders'])
            st.metric("Return Rate", f"{data['return_rate']:.1%}")
            st.write("Top Returned Products:", data['top_returned_products'])
        else:
            st.error("Error fetching data")
    except Exception as e:
        st.error(f"Connection failed: {e}")
