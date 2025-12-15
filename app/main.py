from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router
from app.api.routes.comments import router as comments_router
from app.api.routes.users import router as users_router

app = FastAPI(title="Support Ticket Backend")

app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(users_router, prefix="/users", tags=["users"])

# @app.on_event("startup")
# def startup_event():
#     try:
#         from app.db.engine import init_db
#         init_db()
#     except Exception:
#         # DB not configured or import failed; ignore for in-memory mode
#         print("Database initialization skipped")
#         pass
