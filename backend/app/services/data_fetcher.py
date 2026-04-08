"""
Economic indicator data fetcher.
Uses realistic mock data that can be replaced with real API calls.
"""
from typing import Dict, Any, Optional


ECONOMIC_DATA: Dict[str, Dict[str, Any]] = {
    "EUR": {
        "interest_rate": 4.25,
        "inflation_rate": 2.4,
        "gdp_growth": 0.4,
        "unemployment_rate": 6.1,
        "central_bank": "European Central Bank (ECB)",
        "last_policy_decision": "Hold at 4.25% - September 2024",
        "next_policy_decision": "October 2024",
        "currency_name": "Euro",
        "country": "Eurozone",
    },
    "USD": {
        "interest_rate": 5.25,
        "inflation_rate": 3.2,
        "gdp_growth": 2.1,
        "unemployment_rate": 3.8,
        "central_bank": "Federal Reserve (Fed)",
        "last_policy_decision": "Hold at 5.25-5.50% - September 2024",
        "next_policy_decision": "November 2024",
        "currency_name": "US Dollar",
        "country": "United States",
    },
    "GBP": {
        "interest_rate": 5.25,
        "inflation_rate": 6.7,
        "gdp_growth": 0.2,
        "unemployment_rate": 4.3,
        "central_bank": "Bank of England (BoE)",
        "last_policy_decision": "Hold at 5.25% - September 2024",
        "next_policy_decision": "November 2024",
        "currency_name": "British Pound",
        "country": "United Kingdom",
    },
    "JPY": {
        "interest_rate": -0.1,
        "inflation_rate": 3.2,
        "gdp_growth": 1.5,
        "unemployment_rate": 2.5,
        "central_bank": "Bank of Japan (BoJ)",
        "last_policy_decision": "Hold at -0.1% - September 2024",
        "next_policy_decision": "October 2024",
        "currency_name": "Japanese Yen",
        "country": "Japan",
    },
    "AUD": {
        "interest_rate": 4.35,
        "inflation_rate": 5.4,
        "gdp_growth": 1.1,
        "unemployment_rate": 3.7,
        "central_bank": "Reserve Bank of Australia (RBA)",
        "last_policy_decision": "Hold at 4.35% - October 2024",
        "next_policy_decision": "December 2024",
        "currency_name": "Australian Dollar",
        "country": "Australia",
    },
    "CAD": {
        "interest_rate": 5.0,
        "inflation_rate": 3.8,
        "gdp_growth": 0.6,
        "unemployment_rate": 5.5,
        "central_bank": "Bank of Canada (BoC)",
        "last_policy_decision": "Hold at 5.0% - September 2024",
        "next_policy_decision": "October 2024",
        "currency_name": "Canadian Dollar",
        "country": "Canada",
    },
    "NZD": {
        "interest_rate": 5.5,
        "inflation_rate": 4.0,
        "gdp_growth": 0.3,
        "unemployment_rate": 3.6,
        "central_bank": "Reserve Bank of New Zealand (RBNZ)",
        "last_policy_decision": "Hold at 5.5% - October 2024",
        "next_policy_decision": "November 2024",
        "currency_name": "New Zealand Dollar",
        "country": "New Zealand",
    },
    "INR": {
        "interest_rate": 6.5,
        "inflation_rate": 5.0,
        "gdp_growth": 6.5,
        "unemployment_rate": 7.6,
        "central_bank": "Reserve Bank of India (RBI)",
        "last_policy_decision": "Hold at 6.5% - October 2024",
        "next_policy_decision": "December 2024",
        "currency_name": "Indian Rupee",
        "country": "India",
    },
    "MXN": {
        "interest_rate": 11.25,
        "inflation_rate": 4.6,
        "gdp_growth": 3.1,
        "unemployment_rate": 2.8,
        "central_bank": "Banco de Mexico (Banxico)",
        "last_policy_decision": "Hold at 11.25% - September 2024",
        "next_policy_decision": "November 2024",
        "currency_name": "Mexican Peso",
        "country": "Mexico",
    },
}

SUPPORTED_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD",
    "USDCAD", "NZDUSD", "USDINR", "USDMXN"
]


def get_indicators(currency: str) -> Optional[Dict[str, Any]]:
    """Get economic indicators for a currency."""
    return ECONOMIC_DATA.get(currency.upper())


def get_supported_pairs() -> list:
    """Return list of supported forex pairs."""
    return SUPPORTED_PAIRS


def parse_pair(pair: str):
    """Parse a forex pair into base and quote currencies."""
    pair = pair.upper().strip()
    if len(pair) != 6:
        return None, None
    return pair[:3], pair[3:]
