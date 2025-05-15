from fastapi import APIRouter
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.services.user_service import register_user, login_user

router = APIRouter()

@router.post("/register", summary="Registrar usuario", response_model=UserRead)
def register(user: UserCreate):
    return register_user(user)

@router.post("/login", summary="Autenticar usuario", response_model=Token)
def login(user: UserLogin):
    return login_user(user)