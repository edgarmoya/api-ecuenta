from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.models import User
from app.schemas.user import UserRead

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/me", response_model=UserRead)
def get_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user