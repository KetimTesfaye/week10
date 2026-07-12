 Brent Oil Price Change Point Analysis

 Project Overview
This repository investigates structural breaks and volatility regimes in historical Brent crude oil prices (1987–2022) using Exploratory Data Analysis (EDA) and Bayesian change point detection via PyMC.


 1. Concise Analysis Plan
- Objective: Detect and quantify structural shifts in historical Brent crude oil prices to align macroeconomic shocks with statistical regime changes.
- Phase I (Exploratory Data Analysis): Ingest raw daily price sequences, handle missing observations, and compute stationary logarithmic returns ($\ln(P_t) - \ln(P_{t-1})$) to highlight volatility clustering and extreme return variance.
- Phase II (Bayesian Inference): Fit a Gaussian change point model using PyMC, sampling latent parameters for pre-break mean ($\mu_1$), post-break mean ($\mu_2$), observation noise ($\sigma$), and the discrete structural break index ($\tau$).
- Phase III (Event Alignment & Causal Disclaimers): Map posterior break dates against known historical geopolitical and economic shocks while explicitly documenting the limits of attributing direct causality to temporal correlations.


2. Key Historical Shocks & Event Dataset

 Event ID | Date / Period | Category | Description / Geopolitical Context |
 :---: | :---: | :---: | :--- |
 E1 | 1990-08-02 | Geopolitical | Iraqi invasion of Kuwait, triggering the 1990 oil price shock. |
| E2 | 1997–1998 | Economic | Asian Financial Crisis, causing a collapse in global energy demand. |
| E3 | 2001-09-11 | Geopolitical | 9/11 terrorist attacks, introducing immediate market volatility. |
| E4 | 2003-03-20 | Geopolitical | Invasions of Iraq (Start of the Iraq War). |
| E5 | 2008-07-11 | Economic | Brent price historical peak ($\approx \$147/\text{bbl}$) prior to the Global Financial Crisis. |
| E6 | 2008-12-01 | Economic | Global Financial Crisis nadir as demand plummeted worldwide. |
| E7 | 2011-02-15 | Geopolitical | Arab Spring disruptions affecting Middle Eastern supply lines. |
| E8 | 2014-11-27 | Supply / Market | OPEC decision not to cut production, initiating the 2014–2016 oil glut. |
| E9 | 2020-04-20 | Health / Economic | COVID-19 pandemic global lockdowns and historical demand destruction. |
| E10 | 2022-02-24 | Geopolitical | Russia invades Ukraine, creating a massive European energy supply crunch. |


3. Explicit Assumptions and Limitations on Causal Claims

- Stationarity and Normality Assumptions: The Bayesian Gaussian model assumes that log returns fluctuate around constant regime means ($\mu_1, \mu_2$) with stable variance ($\sigma^2$) inside distinct temporal partitions. Financial time series typically display fat-tailed distributions, skewness, and time-varying stochastic volatility that violate strict normality.
- Correlation vs. Causality Limitation: Identifying a statistical change point index ($\tau$) that temporally aligns with an event from the event table above indicates a high-probability structural break in the mean price level. However, time series correlation does not prove unidirectional causality. Confounding variables, anticipatory market pricing, and overlapping macroeconomic policies mean structural breaks reflect coordinated market regime shifts rather than isolated causal reactions.