from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router
from app.api.routes.comments import router as comments_router
from app.api.routes.users import router as users_router
from app.db.repositories import CommentRepo, TicketRepo, UserRepo
import app.services.ticket_service as ticket_service_mod
import app.services.user_service as user_service_mod
import app.services.comment_service as comment_service_mod

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    print("Starting up the application...")

    comment_repo = CommentRepo()
    ticket_repo = TicketRepo()
    user_repo = UserRepo()

    # Assign singletons on the service modules so dependencies read the initialized instances
    user_service_mod._user_service_singleton = user_service_mod.UserService(repo=user_repo)
    comment_service_mod._comment_service_singleton = comment_service_mod.CommentService(repo=comment_repo)
    ticket_service_mod._ticket_service_singleton = ticket_service_mod.TicketService(repo=ticket_repo, comment_service=comment_service_mod._comment_service_singleton)
    
    yield
    # Shutdown actions
    print("Shutting down the application...")
    
app = FastAPI(title="Support Ticket Backend", lifespan=lifespan)

app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(users_router, prefix="/users", tags=["users"])