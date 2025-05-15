from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.services.user_service import register_user, login_user
from app.db.models import User
from app.core.security import get_current_superuser

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, current_user: User = Depends(get_current_superuser)):
    return register_user(user)

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    return login_user(user)