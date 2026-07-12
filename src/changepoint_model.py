import os
import numpy as np

# Force PyTensor fallback mode to avoid missing C-compiler errors on Windows
os.environ['PYTENSOR_FLAGS'] = 'cxx='
import pymc as pm

def build_and_sample_changepoint_model(prices: np.ndarray, draws: int = 1000, tune: int = 1000):
    """
    Builds and samples a Gaussian Bayesian Change Point model using PyMC.
    """
    n_data = len(prices)
    time_idx = np.arange(n_data)
    
    print(f"⚙️ Building Bayesian Change Point model for {n_data} observations...")
    
    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n_data - 1)
        mu_1 = pm.Normal('mu_1', mu=prices.mean(), sigma=prices.std() * 2)
        mu_2 = pm.Normal('mu_2', mu=prices.mean(), sigma=prices.std() * 2)
        sigma = pm.HalfNormal('sigma', sigma=prices.std())
        
        mu_t = pm.math.switch(time_idx < tau, mu_1, mu_2)
        likelihood = pm.Normal('likelihood', mu=mu_t, sigma=sigma, observed=prices)
        
        print("🚀 Executing MCMC sampling...")
        trace = pm.sample(
            draws=draws, 
            tune=tune, 
            return_inferencedata=True, 
            target_accept=0.8,
            random_seed=42
        )
        
    print("✅ MCMC sampling completed successfully.")
    return model, trace