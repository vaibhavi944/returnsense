import pandas as pd

def rename_cities(file_path):
    df = pd.read_csv(file_path)
    
    city_map = {
        'City35': 'Mumbai', 'City68': 'Delhi', 'City73': 'Bangalore',
        'City37': 'Hyderabad', 'City69': 'Ahmedabad', 'City70': 'Chennai',
        'City86': 'Kolkata', 'City20': 'Pune', 'City84': 'Jaipur',
        'City46': 'Lucknow', 'City16': 'Surat', 'City11': 'Kanpur',
        'City5': 'Nagpur', 'City27': 'Indore', 'City78': 'Thane',
        'City77': 'Bhopal', 'City85': 'Visakhapatnam', 'City44': 'Pimpri-Chinchwad',
        'City59': 'Patna', 'City31': 'Vadodara'
    }
    
    # For cities not in map, just keep original or assign generic
    df['User_Location'] = df['User_Location'].map(lambda x: city_map.get(x, x.replace('City', 'Region-')))
    
    df.to_csv(file_path, index=False)
    print("CSV updated with real Indian city names.")

if __name__ == "__main__":
    rename_cities('data/processed/classified_returns.csv')
