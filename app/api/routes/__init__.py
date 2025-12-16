# API routes package

from app.services.comment_service import CommentService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService

# Try to wire DB-backed repos (Postgres) if available; otherwise fall back to in-memory
try:
    print("Using DB-backed repositories")
    from app.db.engine import init_db
    from app.db.repositories import TicketRepo, CommentRepo, UserRepo
    print("Initializing database...")
    init_db()
except Exception:
    # fallback to in-memory services
    print("Using in-memory repositories")
    comment_service = CommentService()
    user_service = UserService()
    ticket_service = TicketService()