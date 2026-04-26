import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class FeatureBuilder:
    def __init__(self):
        self.product_return_rate = {}
        self.customer_return_rate = {}
        self.category_return_rate = {}
        self.global_mean = 0.0
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.features = []

    def fit(self, train_df: pd.DataFrame):
        # Calculate rates ONLY on training data to prevent leakage
        self.global_mean = train_df['target'].mean()
        
        self.product_return_rate = train_df.groupby('Product_ID')['target'].mean().to_dict()
        self.customer_return_rate = train_df.groupby('User_ID')['target'].mean().to_dict()
        self.category_return_rate = train_df.groupby('Product_Category')['target'].mean().to_dict()

        # Categorical columns to encode
        cat_cols = ['Shipping_Method', 'Payment_Method', 'User_Gender', 'Product_Category']
        for col in cat_cols:
            le = LabelEncoder()
            # fit on train
            if col in train_df.columns:
                le.fit(train_df[col].astype(str).fillna('missing'))
                self.label_encoders[col] = le
        
        # Fit scaler on numerical features
        num_cols = ['Product_Price', 'Order_Quantity', 'Discount_Applied', 'User_Age', 'Order_Value']
        train_features = self._build_raw_features(train_df, is_train=True)
        
        # If order_value not present, calculate it
        if 'Order_Value' not in train_features.columns:
            train_features['Order_Value'] = train_features['Product_Price'] * train_features['Order_Quantity']
            
        self.scaler.fit(train_features[num_cols])
        self.features = train_features.columns.tolist()

    def _build_raw_features(self, df: pd.DataFrame, is_train=False) -> pd.DataFrame:
        df_out = pd.DataFrame(index=df.index)
        
        # Mapping return rates
        if 'Product_ID' in df.columns:
            df_out['product_return_rate'] = df['Product_ID'].map(self.product_return_rate).fillna(self.global_mean)
        else:
            df_out['product_return_rate'] = self.global_mean
            
        if 'User_ID' in df.columns:
            df_out['customer_return_rate'] = df['User_ID'].map(self.customer_return_rate).fillna(self.global_mean)
        elif 'customer_id' in df.columns:
             df_out['customer_return_rate'] = df['customer_id'].map(self.customer_return_rate).fillna(self.global_mean)
        else:
             df_out['customer_return_rate'] = self.global_mean
             
        if 'Product_Category' in df.columns:
            df_out['category_return_rate'] = df['Product_Category'].map(self.category_return_rate).fillna(self.global_mean)
        else:
            df_out['category_return_rate'] = self.global_mean
            
        # Existing numeric features
        num_cols = ['Product_Price', 'Order_Quantity', 'Discount_Applied', 'User_Age', 'Order_Value']
        for col in num_cols:
            if col in df.columns:
                df_out[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df_out[col] = 0
                
        # If Order_Value was missing but Price and Quantity exist, calculate
        if df_out['Order_Value'].sum() == 0 and df_out['Product_Price'].sum() > 0:
            df_out['Order_Value'] = df_out['Product_Price'] * df_out['Order_Quantity']
            
        # avg_product_rating (placeholder if not in dataset)
        if 'avg_product_rating' in df.columns:
             df_out['avg_product_rating'] = pd.to_numeric(df['avg_product_rating'], errors='coerce').fillna(3.0)
        else:
             df_out['avg_product_rating'] = 3.0

        # Sentiment score from confidence if category is bad? Actually, let's just use confidence as sentiment placeholder
        if 'confidence' in df.columns:
            df_out['sentiment_score'] = pd.to_numeric(df['confidence'], errors='coerce').fillna(0.5)
        else:
            df_out['sentiment_score'] = 0.5
            
        # Categorical encoding
        for col, le in self.label_encoders.items():
            if col in df.columns:
                known_classes = set(le.classes_)
                mapped = df[col].astype(str).apply(lambda x: x if x in known_classes else 'missing')
                if 'missing' not in known_classes:
                    df_out[col] = mapped.map(lambda x: le.transform([x])[0] if x in known_classes else 0)
                else:
                    df_out[col] = le.transform(mapped)
            else:
                df_out[col] = 0

        return df_out

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = self._build_raw_features(df)
        num_cols = ['Product_Price', 'Order_Quantity', 'Discount_Applied', 'User_Age', 'Order_Value']
        df_out[num_cols] = self.scaler.transform(df_out[num_cols])
        return df_out
