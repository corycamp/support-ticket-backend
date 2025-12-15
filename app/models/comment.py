from pydantic import BaseModel

class CommentCreate(BaseModel):
    ticket_id: int
    user_id: str
    content: str