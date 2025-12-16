from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from app.models.comment import CommentCreate
from app.services.comment_service import CommentService, get_comment_service

router = APIRouter()

@router.post("/", response_model=dict)
async def create_comment(comment: CommentCreate, comment_service: CommentService = Depends(get_comment_service)):
    saved = await comment_service.create_comment(comment)
    return {"comment_id": saved["id"], "status": "created"}

@router.get("/{comment_id}")
async def get_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
    comment = comment_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.get("/")
async def list_comments(comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.list_comments()

@router.put("/{comment_id}/content", response_model=dict)
async def update_comment_content(comment_id: int, new_content: str, comment_service: CommentService = Depends(get_comment_service)):
    updated_comment = comment_service.update_comment_content(comment_id, new_content)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"comment_id": updated_comment["id"], "new_content": updated_comment["content"]}

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
    deleted = comment_service.delete_comment(comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"id": deleted["id"], "status": "deleted"}