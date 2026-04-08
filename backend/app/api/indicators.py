from fastapi import APIRouter, HTTPException
from app.services.data_fetcher import get_indicators, get_supported_pairs, ECONOMIC_DATA

router = APIRouter()


@router.get("/{currency}")
def get_currency_indicators(currency: str):
    """Get economic indicators for a specific currency (e.g., EUR, USD, GBP)."""
    data = get_indicators(currency)
    if not data:
        available = list(ECONOMIC_DATA.keys())
        raise HTTPException(
            status_code=404,
            detail=f"No data for currency '{currency.upper()}'. Available: {', '.join(available)}"
        )
    return {"currency": currency.upper(), "indicators": data}


@router.get("/")
def list_available_currencies():
    """List all currencies with available economic data."""
    currencies = []
    for code, data in ECONOMIC_DATA.items():
        currencies.append({
            "code": code,
            "name": data["currency_name"],
            "country": data["country"],
            "central_bank": data["central_bank"],
        })
    return {"currencies": currencies}
