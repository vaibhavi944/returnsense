import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_seller_return_history(seller_id: str):
    return f"Seller {seller_id} has a 15% return rate. Most returns are due to 'Sizing' and 'Color Mismatch'."

def get_product_complaints(product_id: str):
    if not product_id: return "No specific product data."
    return f"Product {product_id} complaints: 'Material feels cheap', 'Fades after one wash'."

def generate_recommendations(seller_id: str, product_id: str = None):
    """
    Uses Groq LLM to generate intelligent recommendations.
    Falls back to rules if no API key is found.
    """
    history = get_seller_return_history(seller_id)
    complaints = get_product_complaints(product_id)
    
    # 1. If we HAVE an API Key, use the LLM
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
                "recommendations": ["string", "string"]
            }}
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"Groq Error: {e}")
            # Fallback to rules if LLM fails
    
    # 2. FALLBACK RULES (If no API key or LLM error)
    recommendations = ["Review product descriptions for accuracy", "Ensure high-quality images"]
    priority = "MEDIUM"
    
    if "Sizing" in history:
        priority = "HIGH"
        recommendations = [
            "Add a detailed size chart with measurements.",
            "Include a 'Fit Finder' quiz on the product page.",
            "Encourage customers to post photos in reviews."
        ]
    
    return {
        "priority": priority,
        "recommendations": recommendations
    }
