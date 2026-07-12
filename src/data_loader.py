import os
import pandas as pd
import numpy as np

def load_and_preprocess_brent_data(filepath: str = "data/raw/BrentOilPrices.csv") -> pd.DataFrame:
    """
    Loads raw Brent oil prices CSV, cleans columns, parses dates, sorts chronologically,
    and calculates daily logarithmic returns.
    """
    if not os.path.exists(filepath):
        alt_path = os.path.join("..", filepath)
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            raise FileNotFoundError(f"Could not locate dataset at {filepath}")

    print(f"📂 Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    df.columns = [col.strip() for col in df.columns]
    
    # Parse dates and numeric prices
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    
    # Drop NaNs and sort chronologically
    df_clean = df.dropna().sort_values('Date').reset_index(drop=True)
    
    # Calculate daily log returns: ln(P_t) - ln(P_{t-1})
    df_clean['Log_Return'] = np.log(df_clean['Price']) - np.log(df_clean['Price'].shift(1))
    df_clean = df_clean.dropna().reset_index(drop=True)
    
    print(f"✅ Successfully preprocessed {len(df_clean)} records.")
    return df_clean