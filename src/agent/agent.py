import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import json
import re

def generate_recommendations(seller_id: str, product_id: str = None):
    # Data
    history = f"Seller {seller_id} has a 15% return rate. Most returns are due to 'Sizing' and 'Color Mismatch'."
    complaints = f"Product {product_id} complaints: 'Material feels cheap', 'Fades after one wash'."
    
    # 1. Get Key
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    if api_key:
        try:
            client = Groq(api_key=api_key)
            # We ask for a JSON-like string in the prompt
            prompt = f"""
            Context: {history} {complaints}. 
            Provide 3 specific recommendations to reduce returns. 
            Respond ONLY in this JSON format:
            {{
                "priority": "HIGH",
                "recommendations": ["rec1", "rec2", "rec3"]
            }}
            """
            
            # Use llama-3.1-8b-instant (more reliable)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            
            content = chat_completion.choices[0].message.content
            
            # Clean and parse JSON manually to be safe
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                res = json.loads(json_match.group())
                return {
                    "priority": res.get("priority", "MEDIUM"),
                    "recommendations": res.get("recommendations", []),
                    "source": "Groq Llama 3.1 (Success!)",
                    "v": "1.4"
                }
        except Exception as e:
            return {
                "priority": "HIGH",
                "recommendations": [
                    f"AI Error: {str(e)[:100]}",
                    "Please check sizing charts based on history."
                ],
                "source": "Groq Error (v1.4)",
                "v": "1.4"
            }
            
    return {
        "priority": "HIGH",
        "recommendations": ["No API Key detected."],
        "source": "Fallback Mode",
        "v": "1.4"
    }
