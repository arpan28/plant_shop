# House of Bloom Design Document

## Overview
House of Bloom is a premium plant retail experience inspired by Apple/Ugaoo aesthetics. The stack is:

- **Frontend:** React + Vite + Tailwind-style CSS (custom) served via nginx. The UI fetches hero, categories, collections, and product data from the backend and offers a search-driven discovery experience with categories, best sellers, care guides, and testimonials.
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL. The API serves the same copy plus the catalog derived from a curated CSV. PostgreSQL stores products, categories, users, and browsing history.
- **Auth:** JWT-based with OAuth2 password flow, bcrypt password hashing, and token issuance via FastAPI security utilities. Frontend stores JWT in `localStorage` and sends `Authorization: Bearer <token>` for authenticated endpoints.
- **Deployment:** Docker Compose orchestrates Postgres, backend, and frontend containers with healthchecks. The frontend is built via Vite and served from nginx with `VITE_API_URL` pointed at the backend service.

## Data Model

### Categories
- `id`, `title`, `description`, `image`, `product_count`
- Derived from CSV category path and stored in Postgres.
- Exposed via `/api/categories`.

### Plants
- `id`, `slug`, `name`, `description`, `category_id`, `type`, `price`, `inventory`, `image`, `tags`, `vendor`, `status`.
- Created by parsing `backend/data/plants.csv` on startup and synced into Postgres.
- Searchable via `/api/search?q=...` (name/description/tags) using SQL `LIKE`.

### Users & History
- `User`: `email`, `hashed_password`, timestamps.
- `BrowsingHistory`: `user_id`, `path`, `referrer`, `metadata`, `timestamp`.
- History records appended whenever an authenticated user views a product/section.

## Authentication Flow

1. **Registration** (`POST /api/auth/register`): accepts `email` + `password`, hashes the password with bcrypt, saves the user row.
2. **Login** (`POST /api/auth/login`): verifies password, returns JWT access token signed with HMAC (HS256). Token contains user ID/email and expires in 60 minutes.
3. **Protect endpoints:** Frontend includes JWT in `Authorization` header. Backend uses FastAPI `OAuth2PasswordBearer` to decode and validate tokens.
4. **Token refresh (optional):** Could later add refresh tokens or silent re-auth using embedded expiration field.

## Browsing History Capture
- Specialized endpoint (`POST /api/history`) records current path, referrer, and metadata payload for the authenticated user.
- Frontend calls this API when an authenticated user visits `Shop`, `Product`, or category detail views (or via client instrumentation). Data stored in `browsing_history` table.

## API Surface

| Endpoint | Auth | Description |
| --- | --- | --- |
| `/api/hero` | public | Landing hero copy |
| `/api/collections` | public | Manual collection highlights |
| `/api/categories` | public | Auto-generated categories |
| `/api/products` | public | Product catalog |
| `/api/products/{id}` | public | Product detail |
| `/api/search` | public | Search by name/description/tags |
| `/api/care-guides` | public | Care highlights |
| `/api/testimonials` | public | Testimonials |
| `/api/auth/register` | public | Register new user |
| `/api/auth/login` | public | Login + issue JWT |
| `/api/history` | protected | Save browsing hit for authenticated users |
| `/health` | public | Readiness check for Compose healthchecks |

## Technology & Deployment Notes
- **Docker Compose** uses Postgres + backend + frontend services. Postgres data stored in `postgres-data` volume.
- Backend env `DATABASE_URL=postgresql://house:bloom@postgres:5432/house_of_bloom`.
- Frontend build uses `VITE_API_URL=http://backend:8000` so the compiled app hits backend service names within Compose network.
- Running `docker compose up --build` rebuilds everything; `frontend` rebuild required if React sources change.
- For dev/CI, start backend alone (`uvicorn app.main:app ...`) after running `pip install -r requirements.txt` inside virtualenv.

## Next Steps
1. Finish auth endpoints + user registration flow and browsing history API.
2. Hook up frontend forms (login/register) to backend and store JWT in `localStorage`.
3. Instrument product/category views to post history hits while authenticated.
4. Add secure user profile endpoint (`/api/me`) to fetch saved browsing data or recommendations.
5. Consider refresh tokens or session cookies if we expand beyond SPA.

Let me know if you’d like me to extend this doc with API specs, database diagrams, or integration diagrams for future sprints.