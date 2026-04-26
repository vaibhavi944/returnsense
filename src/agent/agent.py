import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

# Initialize Groq Client safely for both Local and Cloud
def get_groq_client():
    # 1. Try Streamlit Secrets (Cloud)
    if "GROQ_API_KEY" in st.secrets:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # 2. Try Environment Variables (Local)
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return Groq(api_key=api_key)
        
    return None

client = get_groq_client()

def get_seller_return_history(seller_id: str):
    return f"Seller {seller_id} has a 15% return rate. Most returns are due to 'Sizing' and 'Color Mismatch'."

def get_product_complaints(product_id: str):
    if not product_id: return "No specific product data."
    return f"Product {product_id} complaints: 'Material feels cheap', 'Fades after one wash'."

def generate_recommendations(seller_id: str, product_id: str = None):
    history = get_seller_return_history(seller_id)
    complaints = get_product_complaints(product_id)
    
    if client:
        try:
            prompt = f"""
            You are a Senior E-commerce Consultant. 
            Analyze this data and provide 3-4 specific, actionable recommendations to reduce returns.
            
            DATA:
            {history}
            {complaints}
            
            FORMAT:
            Return a JSON object with:
            {{
                "priority": "HIGH/MEDIUM/LOW",
                "recommendations": ["string", "string"],
                "source": "Groq Llama 3"
            }}
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(chat_completion.choices[0].message.content)
        except Exception:
            pass # Fallback to rules if error
    
    # FALLBACK RULES
    recommendations = ["Review product descriptions for accuracy", "Ensure high-quality images"]
    priority = "MEDIUM"
    if "Sizing" in history:
        priority = "HIGH"
        recommendations = [
            "Add a detailed size chart with measurements.",
            "Include a 'Fit Finder' quiz on the product page."
        ]
    
    return {
        "priority": priority,
        "recommendations": recommendations,
        "source": "Rule-based System"
    }
