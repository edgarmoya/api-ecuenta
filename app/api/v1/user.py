from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.models import User
from app.schemas.user import UserRead

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/me", summary="Obtener usuario autenticado", response_model=UserRead)
def get_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user