# Brent Crude Oil Market Intelligence Dashboard 

An interactive full-stack analytics platform built to visualize historical Brent crude oil prices (1987–2022), Bayesian change-point detection outputs, and major geopolitical/economic market shocks.

 What This App Does
Explores Price Trends: Displays over 9,000 days of historical spot prices and volatility metrics through an interactive line chart.
Tracks Market Shocks: Features a timeline of major historical events (such as OPEC decisions, conflicts, and economic crises) that users can filter by category.
Event Highlighting: Clicking on any historical event instantly highlights its specific coordinate on the price chart.

 🛠️ Project Structure

The project is cleanly divided into a Python backend and a React frontend:

```text
week10/
├── app.py                      # Flask REST API backend server
├── requirements.txt            # Python dependencies
├── data/
│   └── raw/
│       └── BrentOilPrices.csv  # Historical Brent spot price dataset
└── client/                     # React + Vite frontend workspace
    ├── package.json            # Node dependencies
    ├── tailwind.config.css     # Styling configuration
    └── src/
        ├── App.jsx             # Main dashboard UI logic
        └── index.css           # Tailwind styling directives