# Investment Journal Dashboard MVP

This repository contains an MVP backend for an options-trade learning dashboard.

## Features
- Ticker fact sheet cache (on-demand create/update)
- Unified news storage format with retention policy (default 90 days)
- Trade journal CRUD-lite (create + list)
- Thesis and post-trade review logging

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints
- `GET /health`
- `POST /company/{ticker}/refresh`
- `GET /company/{ticker}/facts`
- `POST /news/ingest`
- `GET /news/{ticker}`
- `POST /news/{id}/flag`
- `POST /maintenance/news-cleanup`
- `POST /trades`
- `GET /trades`
- `POST /reviews`

## Notes
This MVP intentionally does not auto-generate trade thesis. It provides structured facts and storage so the user writes the thesis.
