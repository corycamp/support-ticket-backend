from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pwdlib import PasswordHash
from app.models.token import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, Token, UserLogin
from datetime import datetime, timedelta, timezone

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")

router = APIRouter()

security = HTTPBearer()

fake_admin_login = {
    "username": "admin123",
    "role": "admin",
    #password is "test123"
    "password": "$argon2id$v=19$m=65536,t=3,p=4$DbYy/8v1GZezaRxfVu5nKw$7/PL82XGJa8FgLTIPU4ZFqOisZtjKfMOpHdIsHnnN+A"
}

fake_user_login = {
    "username": "user123",
    "role": "user",
    #password is "test123"
    "password": "$argon2id$v=19$m=65536,t=3,p=4$DbYy/8v1GZezaRxfVu5nKw$7/PL82XGJa8FgLTIPU4ZFqOisZtjKfMOpHdIsHnnN+A"
}

password_hash = PasswordHash.recommended()

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> Token:
    to_encode = data.copy()
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")

def decode_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def required_role(role: str):
    def role_checker(user: dict = Depends(decode_access_token)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

@router.post("/token")
def get_auth_token(payload: UserLogin):
    if payload.username == fake_admin_login["username"] and verify_password(payload.password, fake_admin_login["password"]):
        return create_access_token(data={"sub": payload.username, "role": fake_admin_login["role"]}, expires_delta=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    elif payload.username == fake_user_login["username"] and verify_password(payload.password, fake_user_login["password"]):
        return create_access_token(data={"sub": payload.username, "role": fake_user_login["role"]}, expires_delta=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")