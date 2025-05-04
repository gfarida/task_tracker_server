from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm

from repositories.user_repository import UserRepository
from schemas import SUser, SUserLogin
from services.auth_service import AuthService



router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: SUserLogin) -> SUser:
    if await UserRepository.find_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = AuthService.hash_password(user.password)
    user_id = await UserRepository.create(user.username, hashed_password)
    return SUser(id=user_id, username=user.username)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserRepository.find_by_username(form_data.username)

    if not user or not AuthService.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = AuthService.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}