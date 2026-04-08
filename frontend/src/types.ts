export interface IndicatorData {
  interest_rate: number;
  inflation_rate: number;
  gdp_growth: number;
  unemployment_rate: number;
  central_bank: string;
  last_policy_decision: string;
  next_policy_decision: string;
  currency_name: string;
  country: string;
}

export interface AnalysisResult {
  id?: number;
  pair: string;
  bias: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  confidence: number;
  analysis_text: string;
  base_indicators: IndicatorData;
  quote_indicators: IndicatorData;
  created_at?: string;
}

export interface HistoryResponse {
  analyses: AnalysisResult[];
  total: number;
}

export interface SupportedPairsResponse {
  pairs: string[];
}
