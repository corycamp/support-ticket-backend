# Support Ticket Backend (scaffold)

A minimal FastAPI backend scaffold for managing support tickets.  
Includes API routes, service layers, authentication, and database support (SQLite for development/tests or Postgres for production).

This scaffold is intended for **local development**, **testing**, and **CI/CD workflows**.

---

## 📂 Project Structure

- `app/api/routes` — API routes (FastAPI endpoints)  
- `app/services` — Business logic / service layer  
- `app/models` — Pydantic models for request/response validation  
- `app/core` — Utilities, constants, and shared logic  
- `tests/unit` — Unit tests (no DB dependency)  
- `tests/integration` — Integration tests (can use SQLite or Postgres)  
- `Dockerfile` — Container definition for the app  
- `docker-compose.yml` — Compose setup for dev and test services  
- `Makefile` — Convenience commands for common tasks  

---

## 🔧 Environment Variables

| Variable            | Required | Default  | Description |
|--------------------|----------|---------|-------------|
| SECRET_KEY          | Yes      | -       | JWT signing secret |
| DATABASE_URL        | No       | SQLite fallback | Database URL (Postgres or SQLite) |
| POSTGRES_USER       | No       | postgres | Postgres DB user (Docker only) |
| POSTGRES_PASSWORD   | No       | postgres | Postgres password (Docker only) |
| POSTGRES_DB         | No       | support_db | Postgres database name (Docker only) |

> For CI/CD, add `SECRET_KEY` and `POSTGRES_PASSWORD` as **Repository Secrets** on GitHub.  
> Do **not** commit credentials or `.env` files.

You can use a local `.env` file for development:

```env
SECRET_KEY=changeme
DATABASE_URL=sqlite:///dev.db
```

And run the server with:

```bash
python -m uvicorn app.main:app --reload --env-file .env
```

---

## 🚀 Quick Start (Local)

1. **Create and activate a virtual environment (recommended)**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. **Install dependencies**

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. **Run the server**

```bash
uvicorn app.main:app --reload
```

Open API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Docker

### Build the Docker image

```bash
docker build -t support-ticket-backend:test .
```

### Run the app container (SQLite fallback if DATABASE_URL is not set)

```bash
docker run --rm -p 8000:8000 support-ticket-backend:test
```

Open API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Docker Compose (Recommended for Dev + Postgres)

```bash
# Build and start dev app + DB
docker compose up --build app db

# Run tests in isolated container
docker compose up --build test
```

> The `test` service automatically sets `PYTHONPATH=/app` to prevent import errors.

---

## 📜 Makefile Convenience Commands

| Command            | Description |
|-------------------|-------------|
| `make build`       | Build the Docker image |
| `make up`          | Start dev app + Postgres via Docker Compose |
| `make down`        | Stop services |
| `make run`         | Run the built image locally |
| `make test`        | Run tests locally (Python or Docker Compose) |
| `make docker-test` | Run tests inside Docker image |
| `make shell`       | Open a shell inside a temporary container |

Example:

```bash
make build
make up
# Visit API docs at http://localhost:8000/docs
```

---

## 🔐 Authentication

- **Token endpoint:** `POST /auth/token`  
- Demo credentials (for development only):

| Username  | Role  | Password |
|-----------|-------|----------|
| admin123  | admin | test123  |
| user123   | user  | test123  |

Use returned bearer token in requests:

```http
Authorization: Bearer <token>
```

> Note: This demo auth is simplistic and intended for testing only.

---

## 🧪 Tests

### Run tests locally

```bash
python -m pytest tests -q
```

- Unit tests run independently of the database.  
- Integration tests will default to SQLite if `DATABASE_URL` is not set.  
- To run integration tests against Postgres, set `DATABASE_URL` to the Postgres instance.

### Run tests inside Docker

```bash
docker compose up --build test
```

- The container automatically sets `PYTHONPATH=/app`.  
- Exits with code `0` if tests pass.

---

## ⚙️ Implementation Notes

- **FastAPI + Pydantic** for API and validation.  
- **SQLAlchemy** optional DB persistence (SQLite for dev/tests, Postgres for production).  
- Repository and service layers abstract DB logic for in-memory or DB-backed storage.  
- Timestamps (`created_at`) are timezone-aware UTC datetimes.

---

## 🔄 CI/CD

- GitHub Actions workflow builds Docker image, starts Postgres, and runs tests inside the container.  
- Mirrors local testing environment for reliable CI.

---

## 🤝 Contributing

Contributions welcome! Open an issue or PR with a clear description and tests.

---

