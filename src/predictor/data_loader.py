import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    # Convert target to binary
    if 'Return_Status' in df.columns:
        df['target'] = (df['Return_Status'] == 'Returned').astype(int)
    return df

def split_data(df: pd.DataFrame, test_size=0.2, random_state=42):
    if 'target' not in df.columns:
        raise ValueError("Target column not found in dataframe.")
        
    X = df.drop(columns=['target'])
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    # Reattach target so feature engineering can calculate aggregates ONLY on train
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    return train_df, test_df
