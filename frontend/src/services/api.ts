import { AnalysisResult, HistoryResponse, SupportedPairsResponse } from '../types';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  analyzePair: (pair: string): Promise<AnalysisResult> =>
    request<AnalysisResult>('/api/analysis/analyze', {
      method: 'POST',
      body: JSON.stringify({ pair }),
    }),

  getHistory: (limit = 10, pair?: string): Promise<HistoryResponse> => {
    const params = new URLSearchParams({ limit: String(limit) });
    if (pair) params.set('pair', pair);
    return request<HistoryResponse>(`/api/analysis/history?${params}`);
  },

  getSupportedPairs: (): Promise<SupportedPairsResponse> =>
    request<SupportedPairsResponse>('/api/pairs/supported'),

  clearCache: (): Promise<{ message: string }> =>
    request<{ message: string }>('/api/analysis/clear-cache', { method: 'POST' }),
};
