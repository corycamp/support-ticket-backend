# Support Ticket Backend (scaffold)

This folder contains a minimal FastAPI backend scaffold with:
- API routes under `app/api/routes`
- Service layer under `app/services`
- Pydantic models under `app/models`
- Core utilities under `app/core`
- Tests under `tests/unit` and `tests/integration`
- `Dockerfile`, GitHub Actions workflow, and Terraform scaffold

Quick run (dev):

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```
