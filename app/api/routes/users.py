from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from app.models.user import UserCreate
from app.services.user_service import UserService, get_user_service

router = APIRouter()


@router.post("/", response_model=dict)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    saved = user_service.create_user(user)
    return {"user_email": saved["email"], "status": "created"}

@router.get("/{user_email}")
async def get_user(user_email: str, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(user_email.lower())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
async def list_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.list_users()
    