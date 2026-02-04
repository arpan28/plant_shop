# House of Bloom API

A small FastAPI service that seeds the plant shop with hero copy, curated collections, products, and care/testimonial content.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Run

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The frontend (Vite) can fetch data from `http://localhost:8000/api/...`. CORS is already enabled for localhost frontend ports.

Update the lists in `app/main.py` when you are ready to replace placeholder content with real plant data and imagery.
