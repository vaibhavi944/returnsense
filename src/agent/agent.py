import os
import pandas as pd
from groq import Groq
import streamlit as st
import json
import re

def get_api_key():
    """
    Safely retrieves the API key without triggering a StreamlitSecretNotFoundError.
    """
    # 1. Try environment variable (Local .env)
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
        
    # 2. Try Streamlit Secrets (Cloud) safely
    try:
        # We check if the secrets object is actually populated
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
        
    return None

def get_seller_metrics(seller_id: str):
    try:
        df = pd.read_csv('data/processed/classified_returns.csv')
        total_orders = len(df)
        return_rate = (df['Return_Status'] == 'Returned').mean()
        top_reasons = df['Return_Reason'].value_counts().head(3).to_dict()
        return f"Seller {seller_id} Stats: Return Rate {return_rate:.1%}, Top Issues: {top_reasons}"
    except:
        return "Seller history unavailable."

def get_product_complaints(product_id: str):
    try:
        df = pd.read_csv('data/processed/classified_returns.csv')
        prod_data = df[df['Product_ID'] == product_id]
        if len(prod_data) > 0:
            rate = (prod_data['Return_Status'] == 'Returned').mean()
            reasons = prod_data['Return_Reason'].unique().tolist()
            return f"Product {product_id} has a {rate:.1%} return rate. Reasons cited: {reasons}"
        return f"Product {product_id} is new or has limited history."
    except:
        return "Product data unavailable."

def generate_recommendations(seller_id: str, product_id: str = None):
    history = get_seller_metrics(seller_id)
    complaints = get_product_complaints(product_id)
    
    api_key = get_api_key()
    
    if api_key:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""
            You are a Senior E-commerce Consultant. 
            Data: {history}. {complaints}.
            Provide 3 actionable business recommendations to reduce returns.
            Respond ONLY in JSON format:
            {{
                "priority": "HIGH/MEDIUM/LOW",
                "recommendations": ["...", "...", "..."]
            }}
            """
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            content = chat_completion.choices[0].message.content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                res = json.loads(json_match.group())
                return {**res, "source": "Groq Llama 3.1", "v": "1.5"}
        except Exception as e:
            return {
                "priority": "MEDIUM",
                "recommendations": [f"LLM Error: {str(e)[:50]}", "Verify product descriptions", "Audit inventory"],
                "source": "Fallback (LLM Failed)",
                "v": "1.5"
            }
            
    return {
        "priority": "MEDIUM",
        "recommendations": ["Review sizing charts", "Improve product descriptions", "Check quality control"],
        "source": "Rule-based Fallback (No Key)",
        "v": "1.5"
    }
