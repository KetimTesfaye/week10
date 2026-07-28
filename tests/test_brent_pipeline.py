"""
Unit testing suite for Brent Crude Oil data pipeline and configuration.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.config import ModelConfig, DEFAULT_DATA_PATH

def test_model_config_defaults() -> None:
    """Test that ModelConfig initializes with correct financial and statistical defaults."""
    config = ModelConfig()
    assert config.random_seed == 42
    assert config.draws == 1000
    assert config.tune == 1000
    assert config.target_accept == 0.90
    assert config.chains == 4
    assert isinstance(config.data_path, Path)

def test_log_return_calculation() -> None:
    """Test logarithmic return transformation accuracy."""
    prices = pd.Series([100.0, 105.0, 102.0])
    log_returns = np.log(prices).diff().dropna()
    
    assert len(log_returns) == 2
    assert log_returns.iloc[0] == pytest.approx(np.log(105.0 / 100.0), rel=1e-3)
    assert log_returns.iloc[1] == pytest.approx(np.log(102.0 / 105.0), rel=1e-3)

def test_data_column_validation() -> None:
    """Test dataframe structural validation logic for price datasets."""
    mock_df = pd.DataFrame({
        "Date": ["1987-05-20", "1987-05-21"],
        "Price": [19.85, 20.10]
    })
    mock_df["Date"] = pd.to_datetime(mock_df["Date"])
    
    assert "Date" in mock_df.columns
    assert "Price" in mock_df.columns
    assert pd.api.types.is_datetime64_any_dtype(mock_df["Date"])
    assert pd.api.types.is_numeric_dtype(mock_df["Price"])

def test_dataframe_sorting() -> None:
    """Test that time series records can be sorted chronologically."""
    mock_df = pd.DataFrame({
        "Date": pd.to_datetime(["1987-05-22", "1987-05-20", "1987-05-21"]),
        "Price": [20.0, 18.0, 19.0]
    })
    sorted_df = mock_df.sort_values("Date").reset_index(drop=True)
    
    assert sorted_df.loc[0, "Price"] == 18.0
    assert sorted_df.loc[2, "Price"] == 20.0

def test_config_path_override() -> None:
    """Test custom path assignment in ModelConfig dataclass."""
    custom_path = Path("custom/path/data.csv")
    config = ModelConfig(data_path=custom_path)
    assert config.data_path == custom_path