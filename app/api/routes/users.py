from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate
from app.api.routes import user_service

router = APIRouter()


@router.post("/", response_model=dict)
async def create_user(user: UserCreate):
    saved = user_service.create_user(user)
    return {"user_email": saved["email"], "status": "created"}

@router.get("/{user_email}")
async def get_user(user_email: str):
    user = await user_service.get_user(user_email.lower())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
async def list_users():
    return await user_service.list_users()
    