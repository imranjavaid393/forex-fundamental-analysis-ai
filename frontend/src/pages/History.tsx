import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { AnalysisResult } from '../types';
import AnalysisDetail from '../components/AnalysisDetail';
import LoadingSpinner from '../components/LoadingSpinner';

const History: React.FC = () => {
  const [analyses, setAnalyses] = useState<AnalysisResult[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<AnalysisResult | null>(null);

  useEffect(() => {
    api.getHistory(20)
      .then((data) => {
        setAnalyses(data.analyses);
        setTotal(data.total);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load history.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading history..." />;
  if (error) return <div className="error-box">{error}</div>;

  return (
    <div className="page history-page">
      <h2>Analysis History ({total} total)</h2>
      {analyses.length === 0 ? (
        <p className="empty-state">No analyses yet. Go to the Dashboard to analyze a pair.</p>
      ) : (
        <div className="history-layout">
          <div className="history-list">
            {analyses.map((a) => (
              <div
                key={a.id}
                className={`history-item ${selected?.id === a.id ? 'active' : ''}`}
                onClick={() => setSelected(a)}
              >
                <div className="history-item-header">
                  <span className="pair-badge">{a.pair}</span>
                  <span className={`bias-label bias-${a.bias.toLowerCase()}`}>{a.bias}</span>
                </div>
                <div className="history-item-meta">
                  <span>{Math.round(a.confidence * 100)}% confidence</span>
                  {a.created_at && (
                    <span>{new Date(a.created_at).toLocaleDateString()}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
          <div className="history-detail">
            {selected ? (
              <AnalysisDetail analysis={selected} />
            ) : (
              <p className="empty-state">Select an analysis from the list to view details.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
