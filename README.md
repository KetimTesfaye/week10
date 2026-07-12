 Brent Oil Price Change Point Analysis

Project Overview
This repository investigates structural breaks and volatility regimes in historical Brent crude oil prices (1987–2022) using Exploratory Data Analysis (EDA) and Bayesian change point detection via PyMC.

Analytical Workflow
1. Data Ingestion & Cleaning: Parsing raw daily prices, enforcing datetime formatting, and dropping missing observations.
2. Exploratory Data Analysis (EDA): - Visualizing raw price super-cycles (e.g., the 2008 peak).
   - Transforming non-stationary prices into stationary daily log returns ($\ln(P_t) - \ln(P_{t-1})$) to observe empirical volatility clustering.
3. Bayesian Change Point Modeling: Utilizing a UCRT64/Python environment to infer latent structural break index ($\tau$) and pre/post-break mean regimes ($\mu_1, \mu_2$).

Core Assumptions & Limitations
- Stationarity: Log returns are assumed to be weakly stationary for variance analysis, though extreme geopolitical/macroeconomic shocks exhibit fat-tailed non-normal behaviors.
- Model Simplification: A single-mean shift model isolates broad regime shifts but does not account for time-varying stochastic volatility (e.g., GARCH effects).