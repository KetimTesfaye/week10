import os
import numpy as np
import pandas as pd
from flask import Flask, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React communication

DATA_PATH = "data/raw/BrentOilPrices.csv"

def load_and_preprocess_brent_data(filepath):
    """Helper function to load and preprocess clean Brent data with log returns."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    df = pd.read_csv(filepath)
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    
    # Ensure Date format and chronological sorting
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Price'])
    
    # Calculate daily log returns for volatility analysis
    df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
    df['Log_Return'].fillna(0, inplace=True)
    return df

def get_cached_data():
    try:
        return load_and_preprocess_brent_data(DATA_PATH)
    except Exception as e:
        print(f"Warning: Could not load clean data: {e}")
        return None

@app.route('/api/prices/historical', methods=['GET'])
def get_historical_prices():
    """Endpoint 1: Historical price data & log returns."""
    df = get_cached_data()
    if df is None:
        abort(500, description="Historical dataset could not be loaded on the server.")
        
    records = []
    for _, row in df.iterrows():
        records.append({
            "date": row['Date'].strftime('%Y-%m-%d'),
            "price": float(row['Price']),
            "log_return": float(row['Log_Return'])
        })
        
    return jsonify({
        "status": "success",
        "count": len(records),
        "data": records
    })

@app.route('/api/model/changepoints', methods=['GET'])
def get_changepoint_results():
    """Endpoint 2: Change point results and estimated regime statistics."""
    changepoints = [
        {
            "event_id": "E8",
            "date": "2014-11-27",
            "tau_index": 6920,
            "mu_before": 78.50,
            "mu_after": 48.20,
            "absolute_change": -30.30,
            "percent_change": -38.6,
            "sigma": 0.021,
            "description": "OPEC declines production cuts, initiating oil glut and price crash."
        },
        {
            "event_id": "E9",
            "date": "2020-04-20",
            "tau_index": 8275,
            "mu_before": 52.10,
            "mu_after": 22.40,
            "absolute_change": -29.70,
            "percent_change": -57.0,
            "sigma": 0.045,
            "description": "COVID-19 pandemic global demand destruction."
        }
    ]
    return jsonify({
        "status": "success",
        "model_type": "Gaussian Bayesian Change Point (PyMC)",
        "changepoints": changepoints
    })

@app.route('/api/events/correlations', methods=['GET'])
def get_event_correlations():
    """Endpoint 3: Event correlation data and key historical shocks."""
    events = [
        {"id": "E1", "date": "1990-08-02", "category": "Geopolitical", "description": "Iraqi invasion of Kuwait, triggering the 1990 oil price shock."},
        {"id": "E2", "date": "1997-11-01", "category": "Economic", "description": "Asian Financial Crisis causing global energy demand contraction."},
        {"id": "E3", "date": "2001-09-11", "category": "Geopolitical", "description": "9/11 attacks introducing immediate short-term market turbulence."},
        {"id": "E4", "date": "2003-03-20", "category": "Geopolitical", "description": "Start of the Iraq War."},
        {"id": "E5", "date": "2008-07-11", "category": "Economic", "description": "Historical Brent price peak prior to Global Financial Crisis."},
        {"id": "E6", "date": "2008-12-01", "category": "Economic", "description": "Global Financial Crisis demand nadir."},
        {"id": "E7", "date": "2011-02-15", "category": "Geopolitical", "description": "Arab Spring supply chain disruptions."},
        {"id": "E8", "date": "2014-11-27", "category": "OPEC Policy", "description": "OPEC declines production cuts, initiating oil glut and price crash."},
        {"id": "E9", "date": "2020-04-20", "category": "Economic Shock", "description": "COVID-19 pandemic global demand destruction."},
        {"id": "E10", "date": "2022-02-24", "category": "Geopolitical", "description": "Russian invasion of Ukraine creating European energy supply crunch."}
    ]
    return jsonify({
        "status": "success",
        "count": len(events),
        "events": events
    })

@app.route('/api/model/explainability', methods=['GET'])
def get_model_explainability():
    """Endpoint 4: Model explainability metrics (SHAP global importance and local drivers)."""
    explainability_data = {
        "status": "success",
        "global_importance": [
            {
                "feature": "Rolling Volatility", 
                "shap_value": 0.42, 
                "description": "Measures historical variance clustering and market turbulence."
            },
            {
                "feature": "Price Momentum", 
                "shap_value": 0.28, 
                "description": "Captures acute short-term price velocity during shocks."
            },
            {
                "feature": "Lagged Price", 
                "shap_value": 0.12, 
                "description": "Represents baseline historical price levels."
            }
        ],
        "local_explanations": {
            "event": "April 2020 Pandemic Crash",
            "contributions": [
                {"feature": "Rolling Volatility (+)", "impact": 0.35, "direction": "positive"},
                {"feature": "Price Momentum (-)", "impact": -0.25, "direction": "negative"},
                {"feature": "Lagged Price (-)", "impact": -0.05, "direction": "negative"}
            ],
            "insight": "Sudden surge in rolling volatility combined with sharp negative momentum triggered the high-risk regime classification."
        }
    }
    return jsonify(explainability_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)