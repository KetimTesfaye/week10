import os
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
from src.data_loader import load_and_preprocess_brent_data
from src.eda_plots import plot_brent_eda
from src.changepoint_model import build_and_sample_changepoint_model

if __name__ == '__main__':
    # 1. Load and Preprocess Data
    df_clean = load_and_preprocess_brent_data("data/raw/BrentOilPrices.csv")
    prices = df_clean['Price'].values
    
    # 2. Generate and Save EDA Plots
    print("📈 Generating EDA visualizations...")
    plot_brent_eda(df_clean, save_path="outputs/eda_brent_plot.png")
    
    # 3. Build and Sample Bayesian Change Point Model
    model, trace = build_and_sample_changepoint_model(prices, draws=1000, tune=1000)
    
    # 4. Summarize and Map Inferred Break Date
    print("📊 Compiling MCMC convergence and posterior summary...")
    summary_df = az.summary(trace, var_names=['mu_1', 'mu_2', 'sigma', 'tau'])
    print(summary_df)
    
    # Programmatically map tau to calendar date
    tau_samples = trace.posterior['tau'].values.flatten()
    median_tau_idx = int(np.median(tau_samples))
    estimated_break_date = df_clean.loc[median_tau_idx, 'Date']
    print(f"🎯 Statistically inferred structural break index (tau): {median_tau_idx}")
    print(f"📅 Corresponding estimated break date: {estimated_break_date.strftime('%Y-%m-%d')}")
    
    # Plot and save posterior distribution of tau
    az.plot_posterior(trace, var_names=['tau'])
    plt.title("Posterior Distribution of Structural Break Index (tau)")
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/posterior_tau_plot.png", dpi=300)
    plt.show()