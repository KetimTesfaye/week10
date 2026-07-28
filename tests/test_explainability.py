"""
Unit tests for SHAP model explainability module.
"""
import pytest
import pandas as pd
import numpy as np
from src.explainability import train_volatility_explainer

def test_train_volatility_explainer() -> None:
    """Test that the SHAP explainer successfully trains and returns valid shapes."""
    # Create mock price history
    dates = pd.date_range(start="2020-01-01", periods=100, freq="D")
    prices = np.linspace(20.0, 50.0, 100) + np.random.normal(0, 1, 100)
    mock_df = pd.DataFrame({"Date": dates, "Price": prices})
    
    explainer, X, shap_values = train_volatility_explainer(mock_df)
    
    assert X.shape[0] > 0
    assert X.shape[1] == 3  # LaggedPrice, PriceMomentum, RollingVolatility
    assert shap_values is not None