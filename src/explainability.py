"""
Model explainability module using SHAP for Brent oil volatility and price regime modeling.
"""
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from typing import Tuple, Any

def train_volatility_explainer(df: pd.DataFrame) -> Tuple[Any, pd.DataFrame, np.ndarray]:
    """
    Train a surrogate tree model on lagged volatility and return features 
    to generate SHAP explanations for non-linear market drivers.
    """
    # Feature engineering from historical prices
    df = df.copy()
    df["LogReturn"] = np.log(df["Price"]).diff()
    df["RollingVolatility"] = df["LogReturn"].rolling(window=30).std()
    df["LaggedPrice"] = df["Price"].shift(1)
    df["PriceMomentum"] = df["Price"] - df["LaggedPrice"]
    
    # Drop NaNs resulting from rolling/lag calculations
    model_df = df.dropna(subset=["RollingVolatility", "LogReturn", "PriceMomentum"]).copy()
    
    X = model_df[["LaggedPrice", "PriceMomentum", "RollingVolatility"]]
    y = model_df["RollingVolatility"]
    
    # Train surrogate model
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X, y)
    
    # Compute SHAP values
    explainer = shap.TreeExplainer(regressor)
    shap_values = explainer(X)
    
    return explainer, X, shap_values

def generate_global_shap_plot(shap_values: Any, X: pd.DataFrame, output_path: str = "outputs/shap_global.png") -> None:
    """Generate and save the global SHAP summary plot answering 'Which features matter most globally?'."""
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)
    plt.title("Global Feature Importance (SHAP Summary)", fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def generate_local_shap_explanation(explainer: Any, X: pd.DataFrame, index: int = 0) -> None:
    """Explain why the model made a specific prediction for a given market day."""
    # This answers: 'Why did the model make this specific prediction?'
    single_instance = X.iloc[[index]]
    shap_val_single = explainer(single_instance)
    print(f"Local SHAP explanation generated for index {index}:")
    print(shap_val_single.values)