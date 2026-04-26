import pandas as pd

def rename_all_cities(file_path):
    df = pd.read_csv(file_path)
    
    # List of 100 Real Indian Cities (Top Tier to Tier 2)
    indian_cities = [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur",
        "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara",
        "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar", "Varanasi",
        "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", "Ranchi", "Howrah", "Jabalpur", "Gwalior",
        "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubli-Dharwad", "Bareilly",
        "Moradabad", "Mysore", "Gurgaon", "Aligarh", "Jalandhar", "Tiruchirappalli", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Warangal",
        "Guntur", "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Cuttack",
        "Firozabad", "Kochi", "Nellore", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Rourkela", "Nanded", "Kolhapur",
        "Ajmer", "Akola", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu",
        "Sangli-Miraj & Kupwad", "Mangalore", "Erode", "Belgaum", "Ambattur", "Tirunelveli", "Malegaon", "Gaya", "Jalgaon", "Udaipur"
    ]
    
    # Get unique current city names (City0, City1, etc.)
    # Note: Some might already be renamed or start with Region-
    current_cities = sorted(df['User_Location'].unique())
    
    city_map = {}
    for i, city_name in enumerate(current_cities):
        if i < len(indian_cities):
            city_map[city_name] = indian_cities[i]
        else:
            # If for some reason we have more than 100, just keep the mapped version or use a backup
            city_map[city_name] = f"Locality-{i}"

    df['User_Location'] = df['User_Location'].map(city_map)
    
    df.to_csv(file_path, index=False)
    print(f"Success: All 100 locations mapped to real Indian cities.")

if __name__ == "__main__":
    rename_all_cities('data/processed/classified_returns.csv')
