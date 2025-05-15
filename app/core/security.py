from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from app.core.config import settings
from app.db.models import User
from sqlmodel import Session, select
from app.db.database import engine
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

def get_password_hash(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt

    Args:
        password (str): The plaintext password

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> User:
    """
    Retrieves the current authenticated user based on the provided token

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token credentials

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist
    """
    token = credentials.credentials
    username = decode_access_token(token)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """
    Ensures the current user has superuser privileges

    Args:
        current_user (User): The currently authenticated user

    Returns:
        User: The superuser

    Raises:
        HTTPException: If the user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes. Solo disponible por el superusuario",
        )
    return current_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password

    Args:
        plain_password (str): The user's entered password
        hashed_password (str): The stored hashed password

    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Creates a JWT access token with expiration

    Args:
        data (dict): The payload to encode into the token

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[str]:
    """
    Decodes a JWT access token and retrieves the username

    Args:
        token (str): The JWT token string

    Returns:
        Optional[str]: The username if valid

    Raises:
        HTTPException: If the token is expired or invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )