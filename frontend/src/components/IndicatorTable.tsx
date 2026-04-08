import React from 'react';
import { IndicatorData } from '../types';

interface IndicatorTableProps {
  baseCurrency: string;
  quoteCurrency: string;
  baseIndicators: IndicatorData;
  quoteIndicators: IndicatorData;
}

const fmt = (val: number, suffix = '%') => `${val}${suffix}`;

const IndicatorTable: React.FC<IndicatorTableProps> = ({
  baseCurrency,
  quoteCurrency,
  baseIndicators,
  quoteIndicators,
}) => {
  const rows = [
    {
      label: 'Interest Rate',
      base: fmt(baseIndicators.interest_rate),
      quote: fmt(quoteIndicators.interest_rate),
      favor: baseIndicators.interest_rate > quoteIndicators.interest_rate
        ? baseCurrency
        : quoteIndicators.interest_rate > baseIndicators.interest_rate
        ? quoteCurrency
        : 'Neutral',
    },
    {
      label: 'Inflation Rate',
      base: fmt(baseIndicators.inflation_rate),
      quote: fmt(quoteIndicators.inflation_rate),
      favor: baseIndicators.inflation_rate < quoteIndicators.inflation_rate
        ? baseCurrency
        : quoteIndicators.inflation_rate < baseIndicators.inflation_rate
        ? quoteCurrency
        : 'Neutral',
    },
    {
      label: 'GDP Growth',
      base: fmt(baseIndicators.gdp_growth),
      quote: fmt(quoteIndicators.gdp_growth),
      favor: baseIndicators.gdp_growth > quoteIndicators.gdp_growth
        ? baseCurrency
        : quoteIndicators.gdp_growth > baseIndicators.gdp_growth
        ? quoteCurrency
        : 'Neutral',
    },
    {
      label: 'Unemployment',
      base: fmt(baseIndicators.unemployment_rate),
      quote: fmt(quoteIndicators.unemployment_rate),
      favor: baseIndicators.unemployment_rate < quoteIndicators.unemployment_rate
        ? baseCurrency
        : quoteIndicators.unemployment_rate < baseIndicators.unemployment_rate
        ? quoteCurrency
        : 'Neutral',
    },
  ];

  return (
    <div className="indicator-table-wrapper">
      <table className="indicator-table">
        <thead>
          <tr>
            <th>Indicator</th>
            <th>{baseCurrency}</th>
            <th>{quoteCurrency}</th>
            <th>Favors</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.label}>
              <td>{row.label}</td>
              <td>{row.base}</td>
              <td>{row.quote}</td>
              <td className={`favor favor-${row.favor === 'Neutral' ? 'neutral' : row.favor === baseCurrency ? 'base' : 'quote'}`}>
                {row.favor}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="central-banks">
        <div className="cb-item">
          <strong>{baseCurrency} Central Bank:</strong> {baseIndicators.central_bank}
          <br />
          <span>Last: {baseIndicators.last_policy_decision}</span>
          <br />
          <span>Next: {baseIndicators.next_policy_decision}</span>
        </div>
        <div className="cb-item">
          <strong>{quoteCurrency} Central Bank:</strong> {quoteIndicators.central_bank}
          <br />
          <span>Last: {quoteIndicators.last_policy_decision}</span>
          <br />
          <span>Next: {quoteIndicators.next_policy_decision}</span>
        </div>
      </div>
    </div>
  );
};

export default IndicatorTable;
