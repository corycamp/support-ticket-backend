# API routes package

from app.services.comment_service import CommentService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService

# Try to wire DB-backed repos (Postgres) if available; otherwise fall back to in-memory
try:
    raise Exception("Force in-memory for now")
    from app.db.engine import init_db
    from app.db.repositories import TicketRepo, CommentRepo, UserRepo
    init_db()
    comment_repo = CommentRepo()
    ticket_repo = TicketRepo()
    user_repo = UserRepo()
    comment_service = CommentService(repo=comment_repo)
    user_service = UserService(repo=user_repo)
    ticket_service = TicketService(comment_service, repo=ticket_repo)
except Exception:
    # fallback to in-memory services
    comment_service = CommentService()
    user_service = UserService()
    ticket_service = TicketService()