import os
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_file_path(filepath: str) -> str:
    """
    Validates if the specified file path exists, checking alternate relative paths if necessary.
    """
    if os.path.exists(filepath):
        return filepath
    
    alt_path = os.path.join("..", filepath)
    if os.path.exists(alt_path):
        return alt_path
        
    alt_parent_path = os.path.join("..", "..", filepath)
    if os.path.exists(alt_parent_path):
        return alt_parent_path
        
    raise FileNotFoundError(f"Critical Error: Unable to locate file at '{filepath}' in any expected directory.")

def safe_load_csv(filepath: str) -> pd.DataFrame:
    """
    Safely loads a CSV file with robust try/except error handling for malformed data or I/O failures.
    """
    try:
        valid_path = validate_file_path(filepath)
        logging.info(f"Attempting to parse CSV securely from: {valid_path}")
        df = pd.read_csv(valid_path)
        return df
    except pd.errors.EmptyDataError:
        logging.error("The provided CSV file is completely empty.")
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Malformed data encountered during parsing: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading the dataset: {e}")
        raise

def compute_log_returns(df: pd.DataFrame, price_col: str = 'Price') -> pd.DataFrame:
    """
    Computes daily logarithmic returns with validation for missing or non-positive price values.
    """
    if price_col not in df.columns:
        raise KeyError(f"Expected column '{price_col}' missing from dataframe.")
        
    df_processed = df.copy()
    df_processed['Price_Clean'] = pd.to_numeric(df_processed[price_col], errors='coerce')
    
    # Check for non-positive values which break log calculations
    if (df_processed['Price_Clean'] <= 0).any():
        logging.warning("Non-positive price entries detected; coercing invalid values to NaN.")
        
    df_processed['Log_Return'] = np.log(df_processed['Price_Clean']) - np.log(df_processed['Price_Clean'].shift(1))
    return df_processed.dropna().reset_index(drop=True)