import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import json

def generate_recommendations(seller_id: str, product_id: str = None):
    # Hard-coded history for demo
    history = f"Seller {seller_id} has a 15% return rate. Most returns are due to 'Sizing' and 'Color Mismatch'."
    complaints = f"Product {product_id} complaints: 'Material feels cheap', 'Fades after one wash'."
    
    # 1. Try to get the Groq Key
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    # 2. If Key exists, try LLM
    if api_key:
        try:
            client = Groq(api_key=api_key)
            prompt = f"Context: {history} {complaints}. Provide 3 short recommendations to reduce returns. Return ONLY a JSON with keys 'priority' and 'recommendations'."
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                response_format={"type": "json_object"}
            )
            res = json.loads(chat_completion.choices[0].message.content)
            return {
                "priority": res.get("priority", "MEDIUM"),
                "recommendations": res.get("recommendations", []),
                "source": "Groq Llama 3 (Live AI)",
                "v": "1.2"
            }
        except Exception:
            pass # Fallback on error
            
    # 3. Final Fallback
    return {
        "priority": "HIGH",
        "recommendations": [
            "Add a detailed size chart with measurements.",
            "Include a 'Fit Finder' quiz on the product page.",
            "Encourage customers to post photos in reviews."
        ],
        "source": "Rule-based Engine (No API Key)",
        "v": "1.2"
    }
