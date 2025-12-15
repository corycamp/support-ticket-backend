from pydantic import BaseModel
from app.models.comment import CommentCreate

class TicketCreate(BaseModel):
    id: int
    title: str
    description: str
    comment: list[CommentCreate] | None = None
    priority: "low" | "medium" | "high"
    status: str | None = None
    created_at: str | None = None
