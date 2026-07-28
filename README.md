Brent Crude Oil Market Intelligence & Bayesian Change-Point Analysis Platform

A production-grade quantitative analytics platform combining exploratory data analysis, Bayesian change-point detection via PyMC, SHAP model interpretability, and a full-stack interactive React dashboard to track macroeconomic risk and structural market shifts.

Business Problem

Global energy investors, commodity traders, and institutional risk managers face extreme market volatility driven by geopolitical conflicts, supply chain disruptions, and sudden demand contractions (e.g., the 2014 OPEC price collapse and the 2020 pandemic crash). Traditional forecasting methods often rely on subjective historical windows, making it difficult to objectively quantify structural market shifts and understand tail-risk drivers.

Solution Overview

This project delivers an end-to-end quantitative platform that:

Objectively Isolates Structural Breaks: Utilizes multi-chain Markov Chain Monte Carlo (MCMC) simulation and Bayesian change-point detection via PyMC to identify exact transition points ($\tau$) where baseline market expectations ($\mu_1, \mu_2$) undergo systematic realignment[cite: 1, 3].
Quantifies Volatility Clustering: Characterizes dynamic variance ($\sigma$) in stationary log returns to understand how exogenous shocks amplify market uncertainty.
Ensures Model Transparency: Integrates SHAP (SHapley Additive exPlanations)to audit global feature importance drivers and provide local event drill-downs for high-risk market shocks.
Bridges Backend to Stakeholders: Deploys a full-stack architecture featuring a Flask REST API and an interactive React/Vite dashboard (`client/`) to visualize real-time analytics and interpretability metrics.

Key Results

Rolling Volatility Dominance: SHAP global evaluations establish that Rolling Volatility is the primary driver of structural risk with a mean absolute impact of 0.42, outperforming short-term price momentum and historical anchors.
Crisis Attribution Accuracy: Local event breakdowns successfully isolate the April 2020 Pandemic Crash, proving that an explosion in market variance (+\approx 0.35) and negative price momentum (-\approx 0.25) triggered high-risk regime classifications.
Full-Stack Integration: Deployed a live REST endpoint (`/api/model/explainability`) connected to a modular React frontend (`ExplainabilityPanel.jsx`), reducing stakeholder reporting friction and enabling real-time risk auditing.

Quick Start

```bash
git clone https://github.com/KetimTesfaye/week10
cd week10
pip install -r requirements.txt
python app.py

(To run the frontend dashboard client):

```bash
cd client
npm install
npm run dev

Project Structure

week10/
├── app.py                     
├── requirements.txt            
├── src/                        
│   ├── data_loader.py          
│   └── changepoint_model.py   
├── client/                     
│   ├── src/
│   │   ├── App.jsx             
│   │   └── components/
│   │       └── ExplainabilityPanel.jsx 
│   └── package.json
├── outputs/                   
└── README.md

Demo

Interactive Dashboard UI: Live full-stack interface connecting the Flask backend to the React frontend[cite: 3]. Access via `http://localhost:5173` when running Vite.
SHAP Explainability Panel: Real-time visual progress bars and risk breakdowns rendering global feature importances and local event attributions.

Technical Details

Data: Historical Brent crude oil daily prices (1987–2022), processed via stationary log return transformations (ln(P_t) - ln(P_{t-1})) and rolling volatility metrics.
Model: Bayesian Change-Point Detection using PyMC / MCMC sampling combined with gradient-boosted risk classifiers evaluated via SHAP interpretability frameworks.
Evaluation: Mean absolute SHAP attribution values, structural break indices (tau), and REST API response validation.

Future Improvements

Automated Unit Testing: Expand test coverage in `tests/` using `pytest` for end-to-end data pipelines and API routes.
CI/CD Automation:** Configure GitHub Actions workflows (`.github/workflows/ci.yml`) to run automated linting and test suites on every push with a live status badge.
Advanced Stress-Testing: Incorporate non-linear interaction profiling to better capture extreme tail-risk saturation effects during unprecedented supply shocks.

Author

Ketim Tesfaye
Role: Generative AI & Machine Learning Engineer | Co-Founder & Lead Engineer
GitHub: [KetimTesfaye](https://www.google.com/search?q=https://github.com/KetimTesfaye)