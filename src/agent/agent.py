import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import json

def get_recommendations_from_ai(history, complaints):
    """
    Tries to talk to Groq. Returns None if it fails.
    """
    # 1. Get the key from Secrets (Cloud) or .env (Local)
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return None
        
    try:
        client = Groq(api_key=api_key)
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
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def generate_recommendations(seller_id: str, product_id: str = None):
    history = f"Seller {seller_id} has a 15% return rate. Most returns are due to 'Sizing' and 'Color Mismatch'."
    complaints = f"Product {product_id} complaints: 'Material feels cheap', 'Fades after one wash'."
    
    # Try the real AI first
    ai_result = get_recommendations_from_ai(history, complaints)
    
    if ai_result:
        return ai_result
        
    # FALLBACK: If AI fails or no key
    return {
        "priority": "HIGH",
        "recommendations": [
            "Add a detailed size chart with measurements.",
            "Include a 'Fit Finder' quiz on the product page.",
            "Encourage customers to post photos in reviews."
        ],
        "source": "Rule-based System (Fallback)"
    }
