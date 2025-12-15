from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router

app = FastAPI(title="Support Ticket Backend")

app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
