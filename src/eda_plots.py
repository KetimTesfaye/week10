import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_brent_eda(df: pd.DataFrame, save_path: str = "outputs/eda_brent_plot.png") -> None:
    """
    Generates and saves an exploratory data analysis plot showing
    raw price macro trends and volatility clustering in log returns.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    
    # Top Panel: Raw Price
    ax1.plot(df['Date'], df['Price'], color='#1f77b4', linewidth=1.2)
    ax1.set_title("Brent Crude Oil Prices: Macro Trends & Shocks (1987 – 2022)", fontsize=13, fontweight='bold')
    ax1.set_ylabel("Price ($/bbl)")
    ax1.grid(True, alpha=0.3)
    
    # Bottom Panel: Log Returns
    ax2.plot(df['Date'], df['Log_Return'], color='#2ca02c', linewidth=0.8, alpha=0.8)
    ax2.set_title("Daily Log Returns: Observed Volatility Clustering", fontsize=13, fontweight='bold')
    ax2.set_ylabel("Log Return")
    ax2.set_xlabel("Date")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    print(f"📊 EDA plot successfully saved to {save_path}")
    plt.close()