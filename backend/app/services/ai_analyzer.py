import json
import logging
from typing import Dict, Any, Tuple
from openai import OpenAI
from app.config import settings
from app.services.data_fetcher import get_indicators, parse_pair

logger = logging.getLogger(__name__)


def calculate_bias(base_data: Dict[str, Any], quote_data: Dict[str, Any]) -> Tuple[str, float]:
    """
    Calculate trading bias based on economic indicators comparison.
    Returns (bias, confidence) where bias is BULLISH/BEARISH/NEUTRAL.
    Higher rates, lower inflation, better GDP growth favor a currency.
    """
    score = 0
    factors = 0

    # Interest rate comparison (higher rate = stronger currency)
    rate_diff = base_data["interest_rate"] - quote_data["interest_rate"]
    if abs(rate_diff) > 0.25:
        score += 1 if rate_diff > 0 else -1
        factors += 1

    # Inflation comparison (lower inflation = stronger currency)
    infl_diff = base_data["inflation_rate"] - quote_data["inflation_rate"]
    if abs(infl_diff) > 0.5:
        score += -1 if infl_diff > 0 else 1
        factors += 1

    # GDP growth comparison (higher growth = stronger currency)
    gdp_diff = base_data["gdp_growth"] - quote_data["gdp_growth"]
    if abs(gdp_diff) > 0.3:
        score += 1 if gdp_diff > 0 else -1
        factors += 1

    # Unemployment comparison (lower unemployment = stronger currency)
    unemp_diff = base_data["unemployment_rate"] - quote_data["unemployment_rate"]
    if abs(unemp_diff) > 0.5:
        score += -1 if unemp_diff > 0 else 1
        factors += 1

    if factors == 0:
        return "NEUTRAL", 0.5

    confidence = abs(score) / factors
    if score > 0:
        bias = "BULLISH"
    elif score < 0:
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"

    return bias, round(confidence, 2)


def get_ai_analysis(pair: str, base_currency: str, quote_currency: str,
                    base_data: Dict[str, Any], quote_data: Dict[str, Any],
                    bias: str, confidence: float) -> str:
    """Get AI-generated analysis text from OpenAI."""
    if not settings.openai_api_key:
        return generate_fallback_analysis(pair, base_currency, quote_currency,
                                          base_data, quote_data, bias, confidence)

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        prompt = f"""You are an expert forex fundamental analyst. Analyze the {pair} currency pair based on the following economic data:

{base_currency} ({base_data['currency_name']}) Indicators:
- Interest Rate: {base_data['interest_rate']}%
- Inflation Rate: {base_data['inflation_rate']}%
- GDP Growth: {base_data['gdp_growth']}%
- Unemployment Rate: {base_data['unemployment_rate']}%
- Central Bank: {base_data['central_bank']}
- Last Policy Decision: {base_data['last_policy_decision']}

{quote_currency} ({quote_data['currency_name']}) Indicators:
- Interest Rate: {quote_data['interest_rate']}%
- Inflation Rate: {quote_data['inflation_rate']}%
- GDP Growth: {quote_data['gdp_growth']}%
- Unemployment Rate: {quote_data['unemployment_rate']}%
- Central Bank: {quote_data['central_bank']}
- Last Policy Decision: {quote_data['last_policy_decision']}

Overall Bias: {bias} (Confidence: {confidence:.0%})

Provide a concise 3-4 paragraph fundamental analysis explaining:
1. The key economic drivers for each currency
2. How the indicators compare
3. The fundamental outlook and reasoning for the {bias} bias
4. Key risks to the thesis

Be specific, professional, and data-driven."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return generate_fallback_analysis(pair, base_currency, quote_currency,
                                          base_data, quote_data, bias, confidence)


def generate_fallback_analysis(pair: str, base_currency: str, quote_currency: str,
                                base_data: Dict[str, Any], quote_data: Dict[str, Any],
                                bias: str, confidence: float) -> str:
    """Generate a rule-based analysis when OpenAI is not available."""
    rate_diff = base_data["interest_rate"] - quote_data["interest_rate"]
    infl_diff = base_data["inflation_rate"] - quote_data["inflation_rate"]
    gdp_diff = base_data["gdp_growth"] - quote_data["gdp_growth"]

    lines = [
        f"**{pair} Fundamental Analysis**\n",
        f"The {pair} pair shows a **{bias}** fundamental bias with {confidence:.0%} confidence "
        f"based on a comparison of key economic indicators.\n",
        f"**Interest Rates:** {base_currency} rate is {base_data['interest_rate']}% vs "
        f"{quote_currency} rate of {quote_data['interest_rate']}% "
        f"({'favoring ' + base_currency if rate_diff > 0 else 'favoring ' + quote_currency if rate_diff < 0 else 'neutral'}). "
        f"{base_data['central_bank']} last decision: {base_data['last_policy_decision']}. "
        f"{quote_data['central_bank']} last decision: {quote_data['last_policy_decision']}.\n",
        f"**Inflation & Growth:** {base_currency} inflation at {base_data['inflation_rate']}% with GDP growth of "
        f"{base_data['gdp_growth']}% vs {quote_currency} inflation at {quote_data['inflation_rate']}% "
        f"with GDP growth of {quote_data['gdp_growth']}%. "
        f"{'Higher GDP growth favors ' + base_currency if gdp_diff > 0.3 else 'Higher GDP growth favors ' + quote_currency if gdp_diff < -0.3 else 'Similar growth profiles'}.\n",
        f"**Unemployment:** {base_currency} unemployment at {base_data['unemployment_rate']}% vs "
        f"{quote_currency} at {quote_data['unemployment_rate']}%. "
        f"Lower unemployment generally supports currency strength.\n",
        f"**Risk Factors:** Monitor upcoming central bank decisions — "
        f"{base_currency}: {base_data['next_policy_decision']}, "
        f"{quote_currency}: {quote_data['next_policy_decision']}. "
        f"Any shift in monetary policy stance could alter the fundamental outlook.",
    ]
    return "\n".join(lines)


def analyze_pair(pair: str) -> Dict[str, Any]:
    """Main function to analyze a forex pair."""
    base_currency, quote_currency = parse_pair(pair)
    if not base_currency:
        raise ValueError(f"Invalid pair format: {pair}")

    base_data = get_indicators(base_currency)
    quote_data = get_indicators(quote_currency)

    if not base_data:
        raise ValueError(f"No data available for currency: {base_currency}")
    if not quote_data:
        raise ValueError(f"No data available for currency: {quote_currency}")

    bias, confidence = calculate_bias(base_data, quote_data)
    analysis_text = get_ai_analysis(pair, base_currency, quote_currency,
                                     base_data, quote_data, bias, confidence)

    return {
        "pair": pair.upper(),
        "bias": bias,
        "confidence": confidence,
        "analysis_text": analysis_text,
        "base_currency": base_currency,
        "quote_currency": quote_currency,
        "base_indicators": base_data,
        "quote_indicators": quote_data,
    }
