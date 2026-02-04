# House of Bloom API

A small FastAPI service that seeds the plant shop with hero copy, curated collections, and the plant catalog you provided.

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

The API now persists categories and products inside PostgreSQL. Update `backend/data/plants.csv` to refresh the catalog, then restart the backend; the CSV is reloaded at startup, repopulating both the `plants` and `categories` tables.

## Data sources

- The master plant catalog lives in `backend/data/plants.csv`. Update this CSV to add new plants, categories, pricing, or imagery. When you change the CSV, the backend automatically reloads its dataset on restart.
- `app/data_loader.py` converts the CSV rows into the `PLANTS` list and derives `CATEGORIES` (the UI expects a category for every plant).
- `app/db.py` + `app/models.py` map the catalog to PostgreSQL tables; the startup event truncates and repopulates them with each run.

## API Endpoints

| Endpoint | Description |
| --- | --- |
| `GET /api/hero` | Hero copy for the landing page. |
| `GET /api/collections` | Curated collection highlights (manually authored, stays in the code). |
| `GET /api/categories` | Dynamically generated categories derived from the CSV. |
| `GET /api/products` | All plants from the CSV (id, name, images, category, etc.). |
| `GET /api/products/{product_id}` | Lookup an individual plant by the integer `id`. |
| `GET /api/search?q=<term>` | Full-text-ish search on name/description/tags. Returns `[]` when the query is empty. |
| `GET /api/care-guides` | Care copy for the “House of care” section. |
| `GET /api/testimonials` | Testimonials. |
| `GET /health` | Lightweight readiness probe used by Docker Compose. |

## Database configuration

The default Postgres connection string is `postgresql://house:bloom@postgres:5432/house_of_bloom`. In local development you can override it via `DATABASE_URL`. The app creates the required tables at startup.

## Docker deployment

The project root already contains a `docker-compose.yml` that builds the FastAPI backend, PostgreSQL, and the Vite frontend together. Run the following from the repo root to start the stack:

```bash
cd /path/to/house_of_bloom
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:4173` (served by nginx after the Vite build). The frontend is configured with `VITE_API_URL=http://backend:8000` so it automatically talks to the backend container.

Need to update the plant catalog or add categories? Edit `backend/data/plants.csv` and restart the backend container (`docker compose up --build backend`).
