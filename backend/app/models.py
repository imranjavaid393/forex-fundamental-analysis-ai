from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AnalysisRequest(BaseModel):
    pair: str


class IndicatorData(BaseModel):
    interest_rate: float
    inflation_rate: float
    gdp_growth: float
    unemployment_rate: float
    central_bank: str
    last_policy_decision: str
    next_policy_decision: str


class AnalysisResponse(BaseModel):
    id: Optional[int] = None
    pair: str
    bias: str
    confidence: float
    analysis_text: str
    base_indicators: Dict[str, Any]
    quote_indicators: Dict[str, Any]
    created_at: Optional[datetime] = None


class HistoryResponse(BaseModel):
    analyses: list
    total: int


class SupportedPairsResponse(BaseModel):
    pairs: list
