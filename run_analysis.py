import os
import pandas as pd
import numpy as np
from src.changepoint_model import build_and_sample_changepoint_model
import arviz as az
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # 1. Load Data
    DATA_PATH = os.path.join('data', 'raw', 'BrentOilPrices.csv')
    if not os.path.exists(DATA_PATH):
        DATA_PATH = "../data/raw/BrentOilPrices.csv"

    print("📂 Loading data...")
    df = pd.read_csv(DATA_PATH)
    df.columns = [col.strip() for col in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Clean and sort
    df_clean = df.dropna().sort_values('Date').reset_index(drop=True)
    prices = df_clean['Price'].values
    dates = df_clean['Date'].values

    # 2. Run Modular Bayesian Change Point Model
    model, trace = build_and_sample_changepoint_model(prices, draws=500, tune=500)

    # 3. Analyze Convergence & Output
    print("📊 Generating convergence summary and posterior plots...")
    summary = az.summary(trace, var_names=['mu_1', 'mu_2', 'sigma', 'tau'])
    print(summary)

    # Plot posterior distribution of tau
    az.plot_posterior(trace, var_names=['tau'])
    plt.title("Posterior Distribution of Change Point (tau Index)")
    plt.tight_layout()
    plt.show()