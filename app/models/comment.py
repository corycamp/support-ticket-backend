from pydantic import BaseModel

class CommentCreate(BaseModel):
    comment_id: int
    ticket_id: int
    user_id: int
    content: str