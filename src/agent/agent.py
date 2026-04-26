import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import json

def generate_recommendations(seller_id: str, product_id: str = None):
    # Data for the prompt
    history = f"Seller {seller_id} has a 15% return rate. Most returns are due to 'Sizing' and 'Color Mismatch'."
    complaints = f"Product {product_id} complaints: 'Material feels cheap', 'Fades after one wash'."
    
    # 1. Get the key
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    # 2. Try the LLM
    if api_key:
        try:
            client = Groq(api_key=api_key)
            prompt = f"Context: {history} {complaints}. Give 3 recommendations to reduce returns. JSON format with 'priority' and 'recommendations' keys."
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                response_format={"type": "json_object"}
            )
            res = json.loads(chat_completion.choices[0].message.content)
            return {
                "priority": res.get("priority", "MEDIUM"),
                "recommendations": res.get("recommendations", []),
                "source": "Groq Llama 3 (Success!)",
                "v": "1.3"
            }
        except Exception as e:
            # If the API call fails, tell us why in the source label
            return {
                "priority": "HIGH",
                "recommendations": [
                    "Check product descriptions (Fallback)",
                    "Verify sizing charts (Fallback)"
                ],
                "source": f"Groq Error: {str(e)[:50]}",
                "v": "1.3"
            }
            
    # 3. No Key at all
    return {
        "priority": "HIGH",
        "recommendations": ["No API Key detected. Please add it to Streamlit Secrets."],
        "source": "No API Key",
        "v": "1.3"
    }
