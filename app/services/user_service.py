from app.db.models import User
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from sqlmodel import Session, select
from app.db.database import engine
from fastapi import HTTPException

def register_user(user: UserCreate) -> UserRead:
    """
    Registers a new user in the system.

    Args:
        user (UserCreate): Object containing the new user's data

    Returns:
        UserRead: A validated Pydantic model representing the stored user
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, full_name=user.full_name, hashed_password=hashed_password)
    with Session(engine) as session:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return UserRead.model_validate(db_user)

def login_user(user: UserLogin) -> Token:
    """
    Authenticates a user by verifying their credentials and generates an access token

    Args:
        user (UserLogin): Object containing the credentials

    Returns:
        Token: A token object containing the access token and its type
    
    Raises:
        HTTPException: If the credentials are incorrect or the user does not exist.
    """
    with Session(engine) as session:
        db_user = session.exec(select(User).where(User.username == user.username)).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Credenciales incorrectas")
        access_token = create_access_token({"sub": db_user.username})
        return Token(access_token=access_token, token_type='bearer')