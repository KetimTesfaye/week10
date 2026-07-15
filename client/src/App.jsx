import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceDot } from 'recharts';
import { TrendingUp, AlertTriangle, Filter, Calendar } from 'lucide-react';

function App() {
  const [historicalData, setHistoricalData] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [activeEvent, setActiveEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      axios.get('http://localhost:5000/api/prices/historical'),
      axios.get('http://localhost:5000/api/events/correlations')
    ])
      .then(([priceRes, eventRes]) => {
        setHistoricalData(priceRes.data.data || []);
        setEvents(eventRes.data.events || []);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const filteredEvents = selectedCategory === 'All' 
    ? events 
    : events.filter(e => e.category === selectedCategory);

  const activePricePoint = activeEvent 
    ? historicalData.find(d => d.date === activeEvent.date)
    : null;

  return (
    <div className="min-h-screen bg-slate-100 p-6 font-sans text-slate-900">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <header className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Brent Crude Oil Market Intelligence</h1>
            <p className="text-sm text-slate-500">Bayesian Change Point & Geopolitical Event Correlation Dashboard</p>
          </div>
          <div className="flex items-center gap-2 bg-blue-50 text-blue-700 px-3 py-1.5 rounded-lg text-sm font-medium">
            <TrendingUp size={18} /> Flask & Vite Linked
          </div>
        </header>

        {loading && <div className="p-8 text-center bg-white rounded-xl shadow-sm">Loading market time-series & shock data...</div>}
        {error && <div className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-200">Connection Error: {error} (Ensure `python app.py` is active)</div>}

        {!loading && !error && (
          <>
            {/* Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <div className="flex justify-between items-center text-slate-500 mb-2">
                  <span className="text-sm font-medium">Tracked Shocks</span>
                  <Calendar size={20} className="text-blue-500" />
                </div>
                <div className="text-2xl font-bold">{events.length} Events</div>
              </div>
              <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <div className="flex justify-between items-center text-slate-500 mb-2">
                  <span className="text-sm font-medium">Historical Records</span>
                  <TrendingUp size={20} className="text-emerald-500" />
                </div>
                <div className="text-2xl font-bold">{historicalData.length} Days</div>
              </div>
              <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <div className="flex justify-between items-center text-slate-500 mb-2">
                  <span className="text-sm font-medium">Active Selection</span>
                  <AlertTriangle size={20} className="text-amber-500" />
                </div>
                <div className="text-lg font-semibold truncate">
                  {activeEvent ? `${activeEvent.date}: $${activePricePoint?.price || 'N/A'}` : 'Click an event below'}
                </div>
              </div>
            </div>

            {/* Price Chart Panel */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
              <h2 className="text-lg font-bold text-slate-800">Historical Price Trajectory & Shocks</h2>
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={historicalData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="date" tick={{ fontSize: 12 }} interval={Math.floor(historicalData.length / 10)} />
                    <YAxis tick={{ fontSize: 12 }} domain={['auto', 'auto']} />
                    <Tooltip />
                    <Line type="monotone" dataKey="price" stroke="#2563eb" strokeWidth={1.5} dot={false} />
                    {activePricePoint && (
                      <ReferenceDot x={activePricePoint.date} y={activePricePoint.price} r={6} fill="#dc2626" stroke="#white" />
                    )}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Event Filtering & Interaction Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Category Filter */}
              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4 h-fit">
                <div className="flex items-center gap-2 font-bold text-slate-800">
                  <Filter size={18} /> Category Filter
                </div>
                <div className="flex flex-wrap gap-2">
                  {['All', 'Geopolitical', 'Economic', 'OPEC Policy'].map(cat => (
                    <button
                      key={cat}
                      onClick={() => setSelectedCategory(cat)}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                        selectedCategory === cat 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                    >
                      {cat}
                    </button>
                  ))}
                </div>
              </div>

              {/* Event Interactive List */}
              <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
                <h2 className="text-lg font-bold text-slate-800">Market Shocks Timeline</h2>
                <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
                  {filteredEvents.map(ev => (
                    <div 
                      key={ev.id}
                      onClick={() => setActiveEvent(ev)}
                      className={`p-3.5 rounded-lg border cursor-pointer transition-all ${
                        activeEvent?.id === ev.id 
                          ? 'bg-blue-50/70 border-blue-300 ring-1 ring-blue-300' 
                          : 'bg-slate-50/50 border-slate-200 hover:bg-slate-100/80'
                      }`}
                    >
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-semibold text-blue-600 text-sm">{ev.date}</span>
                        <span className="text-xs px-2 py-0.5 bg-slate-200 text-slate-700 rounded font-medium">{ev.category}</span>
                      </div>
                      <p className="text-sm text-slate-700">{ev.description}</p>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;