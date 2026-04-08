import json
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Analysis
from app.models import AnalysisRequest, AnalysisResponse
from app.services.ai_analyzer import analyze_pair
from app.services.cache_manager import cache_manager
from app.services.data_fetcher import get_supported_pairs, SUPPORTED_PAIRS

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_forex_pair(request: AnalysisRequest, db: Session = Depends(get_db)):
    """Analyze a forex pair using fundamental economic data and AI."""
    pair = request.pair.upper().strip()

    # Validate pair
    if pair not in SUPPORTED_PAIRS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported pair '{pair}'. Supported pairs: {', '.join(SUPPORTED_PAIRS)}"
        )

    # Check cache
    cache_key = f"analysis:{pair}"
    cached = cache_manager.get(db, cache_key)
    if cached:
        logger.info(f"Returning cached analysis for {pair}")
        return AnalysisResponse(**cached)

    try:
        result = analyze_pair(pair)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error for {pair}: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")

    # Store in database
    indicators_data = json.dumps({
        "base": result["base_indicators"],
        "quote": result["quote_indicators"],
    })
    db_analysis = Analysis(
        pair=result["pair"],
        bias=result["bias"],
        confidence=result["confidence"],
        analysis_text=result["analysis_text"],
        indicators_data=indicators_data,
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    response = AnalysisResponse(
        id=db_analysis.id,
        pair=db_analysis.pair,
        bias=db_analysis.bias,
        confidence=db_analysis.confidence,
        analysis_text=db_analysis.analysis_text,
        base_indicators=result["base_indicators"],
        quote_indicators=result["quote_indicators"],
        created_at=db_analysis.created_at,
    )

    # Cache the result
    cache_manager.set(db, cache_key, response.model_dump(mode="json"))

    return response


@router.get("/history")
def get_analysis_history(
    limit: int = Query(default=10, ge=1, le=100),
    pair: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    """Get analysis history from database."""
    query = db.query(Analysis).order_by(Analysis.created_at.desc())
    if pair:
        query = query.filter(Analysis.pair == pair.upper())
    total = query.count()
    analyses = query.limit(limit).all()

    result = []
    for a in analyses:
        indicators = json.loads(a.indicators_data)
        result.append({
            "id": a.id,
            "pair": a.pair,
            "bias": a.bias,
            "confidence": a.confidence,
            "analysis_text": a.analysis_text,
            "base_indicators": indicators.get("base", {}),
            "quote_indicators": indicators.get("quote", {}),
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })

    return {"analyses": result, "total": total}


@router.post("/clear-cache")
def clear_cache(db: Session = Depends(get_db)):
    """Clear all cached data."""
    count = cache_manager.clear(db)
    return {"message": f"Cache cleared. {count} entries removed."}
