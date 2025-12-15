from fastapi import APIRouter, HTTPException
from app.models.comment import CommentCreate
from app.api.routes import comment_service

router = APIRouter()

@router.post("/", response_model=dict)
async def create_comment(comment: CommentCreate):
    saved = await comment_service.create_comment(comment)
    return {"comment_id": saved["id"], "status": "created"}

@router.get("/{comment_id}")
async def get_comment(comment_id: int):
    comment = comment_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.get("/")
async def list_comments():
    return comment_service.list_comments()