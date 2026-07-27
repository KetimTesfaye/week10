import React from 'react';
import ExplainabilityPanel from './components/ExplainabilityPanel';
// Import your other dashboard components here if you have them separated, 
// e.g., import HistoricalChart from './components/HistoricalChart';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      {/* Dashboard Header */}
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Brent Oil Market Intelligence Dashboard</h1>
        <p className="text-sm text-gray-600">Real-time market analytics, Bayesian change points, and model explainability.</p>
      </header>

      {/* Main Dashboard Grid / Content Area */}
      <main className="space-y-6">
        {/* Placeholder for your existing charts/components */}
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
          <h2 className="text-xl font-bold text-gray-800 mb-2">Historical Price & Regime Overview</h2>
          <p className="text-sm text-gray-500">Your historical price charts and change point timelines render here.</p>
        </div>

        {/* Integrated SHAP Explainability Panel */}
        <ExplainabilityPanel />
      </main>
    </div>
  );
}