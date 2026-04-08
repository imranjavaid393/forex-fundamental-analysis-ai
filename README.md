# Forex Fundamental Analysis AI

An AI-powered forex fundamental analysis system that provides trading bias and direction recommendations based on real economic indicators.

## 🎯 Features

- **AI-Powered Analysis** — Uses OpenAI GPT to interpret economic data (falls back to rule-based analysis without API key)
- **Economic Indicators** — Interest rates, GDP growth, inflation, unemployment for 9 major currencies
- **Trading Bias** — BULLISH / BEARISH / NEUTRAL with confidence scores (0–1)
- **Historical Tracking** — SQLite database stores all past analyses
- **Caching** — 1-hour TTL cache for repeated pair lookups
- **Professional UI** — Dark-themed React + TypeScript dashboard
- **Docker Ready** — One-command deployment with `docker-compose up`

## 🗂 Project Structure

```
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── main.py           # FastAPI app, CORS, rate limiting
│   │   ├── config.py         # pydantic-settings configuration
│   │   ├── models.py         # Pydantic request/response models
│   │   ├── api/
│   │   │   ├── analysis.py   # POST /analyze, GET /history, POST /clear-cache
│   │   │   └── indicators.py # GET /indicators/{currency}
│   │   ├── services/
│   │   │   ├── ai_analyzer.py   # Bias calculation + OpenAI/fallback analysis
│   │   │   ├── data_fetcher.py  # Mock economic data for 9 currencies
│   │   │   └── cache_manager.py # DB-backed TTL cache
│   │   └── database/
│   │       ├── database.py   # SQLAlchemy engine, session, init_db
│   │       └── models.py     # Analysis & CacheEntry ORM models
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/       # Dashboard, AnalysisDetail, IndicatorTable, LoadingSpinner
│   │   ├── pages/            # Home, History
│   │   ├── services/api.ts   # Typed API client
│   │   ├── types.ts          # TypeScript interfaces
│   │   └── styles.css        # Dark theme CSS
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Option A: Docker (Recommended)

```bash
git clone https://github.com/imranjavaid393/forex-fundamental-analysis-ai.git
cd forex-fundamental-analysis-ai

# Optional: add OpenAI key for AI-powered analysis
export OPENAI_API_KEY=sk-your-key-here

docker-compose up
```

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Backend:** http://localhost:8000

### Option B: Manual Setup

**Backend:**
```bash
cd backend
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY (optional)
pip install -r requirements.txt
python main.py
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm start
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analysis/analyze` | Analyze a forex pair |
| `GET` | `/api/analysis/history` | Get analysis history (`?limit=10&pair=EURUSD`) |
| `GET` | `/api/indicators/{currency}` | Get indicators for EUR, USD, GBP, etc. |
| `GET` | `/api/pairs/supported` | List supported pairs |
| `POST` | `/api/analysis/clear-cache` | Clear cache |
| `GET` | `/health` | Health check |

**Example:**
```bash
curl -X POST http://localhost:8000/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{"pair": "EURUSD"}'
```

## 📊 Supported Pairs

`EURUSD` · `GBPUSD` · `USDJPY` · `AUDUSD` · `USDCAD` · `NZDUSD` · `USDINR` · `USDMXN`

## 🔐 Configuration

Create `backend/.env`:

```env
OPENAI_API_KEY=sk-your-openai-api-key
DATABASE_URL=sqlite:///./forex_analysis.db
DEBUG=True
LOG_LEVEL=INFO
CACHE_TTL=3600
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

> **Note:** `OPENAI_API_KEY` is optional. Without it, the app uses a rule-based analysis engine.

## 🏗 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy, Pydantic, slowapi |
| Database | SQLite |
| AI | OpenAI GPT-3.5 (optional) |
| Frontend | React 18, TypeScript |
| Styling | CSS custom properties (dark theme) |
| Deployment | Docker, docker-compose |
AI-powered forex fundamental analysis tool for trading bias prediction
