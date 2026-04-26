def get_seller_return_history(seller_id: str):
    return {"return_rate": "15%", "main_issue": "Sizing issues in apparel"}

def get_product_complaints(product_id: str):
    return ["Runs small", "Color fades after wash"]

def get_category_benchmark(category: str):
    return {"avg_return_rate": "10%"}

def generate_recommendations(seller_id: str, product_id: str = None):
    # Simulating an agent using tools
    seller_info = get_seller_return_history(seller_id)
    
    recommendations = []
    priority = "MEDIUM"
    if "Sizing" in seller_info.get("main_issue", ""):
        priority = "HIGH"
        recommendations.append("Add a detailed size chart to all apparel listings.")
        recommendations.append("Include customer reviews about sizing fit (e.g., runs small).")
        
    if product_id:
        complaints = get_product_complaints(product_id)
        if "Color fades after wash" in complaints:
            recommendations.append("Update care instructions to specify 'Wash in cold water'.")
            
    if not recommendations:
        recommendations = ["Review product descriptions for accuracy", "Ensure high-quality images"]
        
    return {
        "priority": priority,
        "recommendations": recommendations
    }
