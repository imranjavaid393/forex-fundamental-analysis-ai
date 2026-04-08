import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { AnalysisResult } from '../types';
import AnalysisDetail from './AnalysisDetail';
import LoadingSpinner from './LoadingSpinner';

const SUPPORTED_PAIRS = [
  'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD',
  'USDCAD', 'NZDUSD', 'USDINR', 'USDMXN',
];

const Dashboard: React.FC = () => {
  const [selectedPair, setSelectedPair] = useState('EURUSD');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pairs, setPairs] = useState<string[]>(SUPPORTED_PAIRS);

  useEffect(() => {
    api.getSupportedPairs()
      .then((data) => setPairs(data.pairs))
      .catch(() => setPairs(SUPPORTED_PAIRS));
  }, []);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    try {
      const result = await api.analyzePair(selectedPair);
      setAnalysis(result);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="pair-selector">
        <h2>Forex Pair Analysis</h2>
        <div className="selector-row">
          <select
            value={selectedPair}
            onChange={(e) => setSelectedPair(e.target.value)}
            className="pair-select"
          >
            {pairs.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="analyze-btn"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
        <p className="hint">Select a forex pair and click Analyze to get AI-powered fundamental analysis.</p>
      </div>

      {loading && <LoadingSpinner message="Analyzing fundamental data..." />}
      {error && <div className="error-box">{error}</div>}
      {analysis && !loading && <AnalysisDetail analysis={analysis} />}
    </div>
  );
};

export default Dashboard;
