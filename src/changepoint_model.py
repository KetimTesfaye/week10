import os
import numpy as np

# Force PyTensor fallback mode to avoid missing C-compiler errors on Windows
os.environ['PYTENSOR_FLAGS'] = 'cxx='
import pymc as pm

def build_and_sample_changepoint_model(prices: np.ndarray, draws: int = 1000, tune: int = 1000):
    """
    Builds and samples a Gaussian Bayesian Change Point model using PyMC.
    
    Parameters:
    - prices (np.ndarray): 1D array of observed numerical price values.
    - draws (int): Number of posterior samples to draw per chain.
    - tune (int): Number of tuning/warmup steps per chain.
    
    Returns:
    - model (pm.Model): The compiled PyMC model instance.
    - trace (arviz.InferenceData): The MCMC sampling results.
    """
    n_data = len(prices)
    time_idx = np.arange(n_data)
    
    print(f"⚙️ Building Bayesian Change Point model for {n_data} observations...")
    
    with pm.Model() as model:
        # Define the switch point tau as a discrete uniform prior over all time indices
        tau = pm.DiscreteUniform('tau', lower=0, upper=n_data - 1)
        
        # Define before and after regime mean parameters
        mu_1 = pm.Normal('mu_1', mu=prices.mean(), sigma=prices.std() * 2)
        mu_2 = pm.Normal('mu_2', mu=prices.mean(), sigma=prices.std() * 2)
        
        # Define observational noise / volatility prior
        sigma = pm.HalfNormal('sigma', sigma=prices.std())
        
        # Use pm.math.switch to select the active mean parameter based on time index vs tau
        mu_t = pm.math.switch(time_idx < tau, mu_1, mu_2)
        
        # Define the Gaussian likelihood connecting the model to observed prices
        likelihood = pm.Normal('likelihood', mu=mu_t, sigma=sigma, observed=prices)
        
        # Run the MCMC sampler
        print("🚀 Executing MCMC sampling (this may take a moment)...")
        trace = pm.sample(draws=draws, tune=tune, return_inferencedata=True, target_accept=0.9)
        
    print("✅ MCMC sampling completed successfully.")
    return model, trace