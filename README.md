# Support Ticket Backend (scaffold)

This folder contains a minimal FastAPI backend scaffold with:
- API routes under `app/api/routes`
- Service layer under `app/services`
- Pydantic models under `app/models`
- Core utilities under `app/core`
- Tests under `tests/unit` and `tests/integration`
- `Dockerfile`, GitHub Actions workflow, and Terraform scaffold

## 🚀 Quick start (local)

1. Create and activate a virtualenv (recommended):

```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
source .venv/bin/activate  # macOS / Linux
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Set required environment variables (at minimum):

- `SECRET_KEY` — required for signing access tokens
- Optional: `DATABASE_URL` — if omitted the app falls back to a local SQLite DB for development/tests

You can create a `.env` file and use `python -m uvicorn app.main:app --reload --env-file .env`.

4. Run the server:

```bash
uvicorn app.main:app --reload
```

Open the interactive API docs at: http://localhost:8000/docs

---

## 🐳 Docker

Build the image:

```bash
docker build -t support-ticket-backend:test .
```

Run the container (exposes port 8000):

```bash
docker run --rm -p 8000:8000 support-ticket-backend:test
```

- The app will use SQLite when `DATABASE_URL` is not provided.
- Verify the API docs: http://localhost:8000/docs

You can also run tests inside the image:

```bash
docker run --rm support-ticket-backend:test pytest -q
```

### Convenience (Makefile)

A `Makefile` is provided for convenience. Use these targets to speed up common tasks:

- `make build` — build the Docker image
- `make up` — start services via `docker-compose` (includes optional Postgres)
- `make down` — stop services
- `make run` — run the built image locally
- `make test` — run the test suite locally
- `make docker-test` — run tests inside the image
- `make shell` — open a shell inside a temporary container

Example:

```bash
make build
make up
# visit http://localhost:8000/docs
```

---

## 🔐 Authentication

- Token endpoint: `POST /auth/token` (uses test credentials included in `app/api/routes/auth.py` for demo purposes)
  - Demo logins: `admin123` (role: admin), `user123` (role: user). Password is `test123` for both (hashed in code).
- Use the returned bearer token with `Authorization: Bearer <token>` for protected endpoints.

> Note: This demo auth is intentionally simplistic and intended for development and tests only.

---

## 🧪 Tests

Run unit and integration tests locally:

```bash
python -m pytest tests -q
```

Integration tests use the application's DB init routine and will run against the SQLite fallback by default. To run tests against a Postgres DB, set `DATABASE_URL` to point at your test Postgres instance.

---

## ⚙️ Implementation notes

- Uses FastAPI + Pydantic for API and validation.
- Uses SQLAlchemy for optional DB persistence; repository and service layers are implemented so the app can run with either in-memory stores (for unit tests) or DB-backed repos (for integration/production).
- `created_at` timestamps are timezone-aware (UTC) datetimes.

---

## Contributing

Contributions welcome — open an issue or a PR with a clear description and tests.
