import React, { useState, useEffect } from 'react';

export default function ExplainabilityPanel() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/model/explainability')
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Could not fetch explainability data:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-4 bg-white rounded-lg shadow mt-4">Loading Model Explainability...</div>;
  if (!data) return null;

  return (
    <div className="bg-white p-6 rounded-xl shadow-md mt-6 border border-gray-100">
      <h3 className="text-xl font-bold text-gray-800 mb-2">Model Explainability & SHAP Insights</h3>
      <p className="text-sm text-gray-500 mb-4">Transparent audit of global feature drivers and local event predictions.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Global Importance Section */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-3">Global Feature Importance</h4>
          {data.global_importance.map((item, idx) => (
            <div key={idx} className="mb-3">
              <div className="flex justify-between text-sm font-medium text-gray-600 mb-1">
                <span>{item.feature}</span>
                <span>SHAP: {item.shap_value}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${item.shap_value * 100 * 2}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-400 mt-0.5">{item.description}</p>
            </div>
          ))}
        </div>

        {/* Local Prediction Breakdown Section */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Local Event Drill-Down</h4>
          <span className="inline-block px-2.5 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded-full mb-3">
            {data.local_explanations.event}
          </span>
          <p className="text-sm text-gray-600 leading-relaxed bg-white p-3 rounded border border-gray-200">
            {data.local_explanations.insight}
          </p>
        </div>
      </div>
    </div>
  );
}