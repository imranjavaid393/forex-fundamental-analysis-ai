import React from 'react';
import { AnalysisResult } from '../types';
import IndicatorTable from './IndicatorTable';

interface AnalysisDetailProps {
  analysis: AnalysisResult;
}

const BiasLabel: React.FC<{ bias: string }> = ({ bias }) => (
  <span className={`bias-label bias-${bias.toLowerCase()}`}>{bias}</span>
);

const ConfidenceBar: React.FC<{ confidence: number }> = ({ confidence }) => (
  <div className="confidence-bar-wrapper">
    <div className="confidence-bar">
      <div
        className="confidence-fill"
        style={{ width: `${confidence * 100}%` }}
      />
    </div>
    <span className="confidence-text">{Math.round(confidence * 100)}%</span>
  </div>
);

const AnalysisDetail: React.FC<AnalysisDetailProps> = ({ analysis }) => {
  const baseCurrency = analysis.pair.slice(0, 3);
  const quoteCurrency = analysis.pair.slice(3, 6);

  return (
    <div className="analysis-detail">
      <div className="analysis-header">
        <div>
          <h2 className="pair-title">{analysis.pair}</h2>
          {analysis.created_at && (
            <p className="created-at">
              {new Date(analysis.created_at).toLocaleString()}
            </p>
          )}
        </div>
        <div className="bias-section">
          <BiasLabel bias={analysis.bias} />
          <ConfidenceBar confidence={analysis.confidence} />
        </div>
      </div>

      <div className="analysis-body">
        <section className="analysis-section">
          <h3>Economic Indicators Comparison</h3>
          <IndicatorTable
            baseCurrency={baseCurrency}
            quoteCurrency={quoteCurrency}
            baseIndicators={analysis.base_indicators}
            quoteIndicators={analysis.quote_indicators}
          />
        </section>

        <section className="analysis-section">
          <h3>AI Analysis</h3>
          <div className="analysis-text">
            {analysis.analysis_text.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default AnalysisDetail;
