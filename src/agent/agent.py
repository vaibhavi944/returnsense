import os
import pandas as pd
from groq import Groq
import streamlit as st
import json
import re

def get_api_key():
    key = os.getenv("GROQ_API_KEY")
    if key: return key
    try:
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except: pass
    return None

def get_seller_metrics(seller_id: str):
    """
    Retrieves unique stats for a specific city/region to give the AI real context.
    """
    try:
        df = pd.read_csv('data/processed/classified_returns.csv')
        # Filter data for the specific city (Seller proxy)
        city_df = df[df['User_Location'] == seller_id]
        
        if len(city_df) > 0:
            return_rate = (city_df['Return_Status'] == 'Returned').mean()
            top_reasons = city_df[city_df['Return_Status'] == 'Returned']['Return_Reason'].value_counts().head(3).to_dict()
            total_orders = len(city_df)
            return f"City {seller_id} Stats: Total Orders: {total_orders}, Return Rate {return_rate:.1%}, Top Issues: {top_reasons}"
        
        return f"City {seller_id} has limited history in the system."
    except Exception as e:
        return f"Error retrieving city stats: {str(e)}"

def get_product_complaints(product_id: str):
    if not product_id:
        return "No specific product selected. Analysis is based on general category trends."
    try:
        df = pd.read_csv('data/processed/classified_returns.csv')
        prod_data = df[df['Product_ID'] == product_id]
        if len(prod_data) > 0:
            rate = (prod_data['Return_Status'] == 'Returned').mean()
            reasons = prod_data[prod_data['Return_Status'] == 'Returned']['Return_Reason'].unique().tolist()
            return f"Product {product_id} has a {rate:.1%} return rate. Reasons cited by customers: {reasons}"
        return f"Product {product_id} is new or has limited history."
    except:
        return "Product data unavailable."

def generate_recommendations(seller_id: str, product_id: str = None):
    # Now history is UNIQUE to the city picked!
    history = get_seller_metrics(seller_id)
    complaints = get_product_complaints(product_id)
    
    api_key = get_api_key()
    
    if api_key:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""
            You are a Senior E-commerce Strategy Consultant.
            CITY DATA: {history}
            PRODUCT FOCUS: {complaints}
            
            Based on this specific data, provide 3 highly professional, actionable recommendations to reduce returns.
            Respond ONLY in JSON format:
            {{
                "priority": "HIGH/MEDIUM/LOW",
                "recommendations": [
                    {{
                        "action": "Short title of the action",
                        "description": "Detailed explanation of what to do",
                        "metrics": "Expected outcome (e.g. 5% reduction in returns)"
                    }}
                ]
            }}
            """
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"}
            )
            content = chat_completion.choices[0].message.content
            res = json.loads(content)
            return {**res, "source": "Groq Llama 3.1", "v": "1.6"}
        except:
            pass
            
    return {
        "priority": "MEDIUM",
        "recommendations": [
            {"action": "Audit Local Logistics", "description": f"Verify the shipping and handling process in {seller_id} region.", "metrics": "Lower damage-related returns by 8%"}
        ],
        "source": "Rule-based Fallback",
        "v": "1.6"
    }
