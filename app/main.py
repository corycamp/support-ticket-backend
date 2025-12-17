from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router
from app.api.routes.comments import router as comments_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.db.engine import init_db
from app.db import engine as db
from app.db.repositories import CommentRepo, TicketRepo, UserRepo
import app.services.ticket_service as ticket_service_mod
import app.services.user_service as user_service_mod
import app.services.comment_service as comment_service_mod

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    print("Starting up the application...")
    
    try:
        init_db()
        comment_repo = CommentRepo(session_factory=db.SessionLocal)
        ticket_repo = TicketRepo(session_factory=db.SessionLocal)
        user_repo = UserRepo(session_factory=db.SessionLocal)

        # Assign singletons on the service modules so dependencies read the initialized instances
        user_service_mod._user_service_singleton = user_service_mod.UserService(repo=user_repo)
        comment_service_mod._comment_service_singleton = comment_service_mod.CommentService(repo=comment_repo)
        ticket_service_mod._ticket_service_singleton = ticket_service_mod.TicketService(repo=ticket_repo, comment_service=comment_service_mod._comment_service_singleton)
    except Exception as e:
        print(f"Error during database initialization: {e}")
        user_service_mod._user_service_singleton = user_service_mod.UserService()
        comment_service_mod._comment_service_singleton = comment_service_mod.CommentService()
        ticket_service_mod._ticket_service_singleton = ticket_service_mod.TicketService(comment_service=comment_service_mod._comment_service_singleton)
    
    yield
    # Shutdown actions
    print("Shutting down the application...")
    
app = FastAPI(title="Support Ticket Backend", lifespan=lifespan)

app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])