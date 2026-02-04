# House of Bloom

Design-forward plant shop inspired by Apple and Ugaoo, with a React storefront and FastAPI backend.

## Architecture

- **Frontend:** Vite + React (latest). Styled components deliver hero, categories, collection, and product sections, plus a search bar and testimonials.
- **Backend:** FastAPI seeding hero copy, categories, collections, care guides, testimonials, and products. Categories and product data are sourced from `backend/data/plants.csv`, so updating that CSV automatically reshapes the catalog. The backend now persists plant and category data in PostgreSQL (credentials: `postgresql://house:bloom@postgres:5432/house_of_bloom`) and exposes the same JSON endpoints with real rows.
- **Deployment:** `docker-compose up --build` brings both containers up (frontend served via nginx, backend via uvicorn).

## Run with Docker Compose

```bash
cd /path/to/house_of_bloom
docker compose up --build
```

- Backend will be available at `http://localhost:8000` (see `/api/*` endpoints).
- Frontend will serve from `http://localhost:4173`, and Vite is pre-built during the image. The frontend is wired to talk to the backend container at `http://backend:8000` via the `VITE_API_URL` build arg.

## When you need to switch assets

- Replace placeholder Unsplash URLs inside `backend/app/main.py` with your AWS S3 links (or point the frontend directly to a CDN). Updating the data here automatically propagates to the UI because the frontend fetches this list on load.
- To re-build the frontend image after changing any React files, re-run `docker compose up --build` (or `docker compose build frontend`).

## Backend dev mode (without Docker)

See `backend/README.md` for manual setup instructions, the seeded data, and the new `/api/categories` & `/api/search` endpoints.
