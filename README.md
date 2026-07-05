# Smart Money

A mobile-first dashboard that tracks where prediction-market bettors, corporate
insiders, and members of Congress are putting their money — and scores how
strongly the three agree on each stock (the **Conviction Signal**).

No login. Opens straight to the dashboard.

## Stack

- **Frontend**: React 19 + Tailwind CSS 4 (Vite), React Router, localStorage watchlist
- **Backend**: FastAPI + Motor (async MongoDB driver) + APScheduler
- **Data**: Polymarket Gamma API, SEC EDGAR Form 4 filings, House/Senate Stock
  Watcher — all public, no API keys. Each source falls back to clearly-labeled
  sample data if temporarily unreachable, so the app always renders end to end.

## Project layout

```
smart-money/
  backend/            FastAPI app
    app/
      main.py          app + CORS + startup refresh + scheduler
      config.py        env-based settings
      db.py            Mongo collections
      models.py        Pydantic response models
      conviction.py    the Conviction Score formula (see docstring)
      cache.py         refresh-and-store-in-Mongo logic
      routers/         /api/conviction, /polymarket, /insiders, /congress, /meta
      services/        live fetchers (Polymarket, SEC EDGAR, Congress) + sample data
  frontend/            Vite React app (5 tabs + detail views)
  docker-compose.yml   mongo + backend + frontend, one command
```

## Run locally with Docker

```bash
cd smart-money
docker compose up --build
```

- Frontend: http://localhost:4173
- Backend: http://localhost:8000 (docs at /docs)

## Run locally without Docker

**Backend** (needs a MongoDB instance reachable at `MONGO_URI`, e.g. a local
`mongod` or a free MongoDB Atlas cluster):

```bash
cd smart-money/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit MONGO_URI if not using localhost:27017
uvicorn app.main:app --reload
```

**Frontend**:

```bash
cd smart-money/frontend
npm install
cp .env.example .env   # VITE_API_URL, defaults to http://localhost:8000
npm run dev
```

Open http://localhost:5173 on a phone-width viewport (or your phone, via the
"Network" URL Vite prints) to see the mobile-first design.

## The Conviction Score

Documented in full in `backend/app/conviction.py`. Summary: each of the 3
sources produces a lean (bearish..bullish, -1..1) and a strength (0..1) based
on recency + size of recent activity. The combined score rewards signals that
are strong, corroborated by as many of the 3 sources as possible, and backed
by real recent activity — and scores near zero when sources conflict or are
quiet. All three agreeing on direction earns the ⚡ "high conviction" badge.

## Deploying

This is a standard 3-tier app (static frontend, stateless API, database), so
any combination of the usual hosts works:

1. **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas) free tier — create a
   cluster, get a `mongodb+srv://...` connection string.
2. **Backend**: any container/PaaS host (Render, Fly.io, Railway, etc.) — point
   it at the `backend/Dockerfile`, set `MONGO_URI` to your Atlas string and
   `CORS_ORIGINS` to your deployed frontend URL.
3. **Frontend**: any static host (Vercel, Netlify, Cloudflare Pages) — build
   with `VITE_API_URL` set to your deployed backend URL.

## Notes & known limitations

- **SEC EDGAR** requires a descriptive `User-Agent` on every request
  (`SEC_USER_AGENT` env var) and should stay under ~10 req/sec — the fetcher
  respects both.
- **Congress data** (House/Senate Stock Watcher) is disclosed on a legal delay
  of up to ~45 days; the UI surfaces both the transaction date and the
  disclosure date so this is never ambiguous.
- **Polymarket ↔ ticker matching** is a keyword heuristic (`services/ticker_map.py`)
  since Polymarket has no ticker field — it only links a market to a stock when
  the question text names the company. Expect coverage to be sparse for most
  tickers; that's expected, not a bug.
- If a live source is down, that feed serves realistic sample data instead,
  clearly labeled "sample data" in the UI, so the app never shows a broken
  screen end to end.
