import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config import settings
from app.database.database import init_db
from app.api import analysis, indicators

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Forex Fundamental Analysis API...")
    init_db()
    logger.info("Database initialized.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Forex Fundamental Analysis AI",
    description="AI-powered forex fundamental analysis using economic indicators",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(indicators.router, prefix="/api/indicators", tags=["Indicators"])


@app.get("/")
def root():
    return {
        "message": "Forex Fundamental Analysis AI API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/pairs/supported")
def get_supported_pairs():
    from app.services.data_fetcher import get_supported_pairs as fetch_pairs
    return {"pairs": fetch_pairs()}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
