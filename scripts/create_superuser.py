import os
from sqlmodel import Session, select
from app.db.models import User
from app.db import engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_superuser():
    username = os.getenv("SUPERUSER_USERNAME")
    password = os.getenv("SUPERUSER_PASSWORD")
    full_name = os.getenv("SUPERUSER_FULLNAME", "Superusuario")

    if not username or not password:
        print("Faltan variables de entorno para el superusuario.")
        return

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            print("El superusuario ya existe.")
            return

        hashed_password = pwd_context.hash(password)
        superuser = User(
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
            is_superuser=True,
        )
        session.add(superuser)
        session.commit()
        print("Superusuario creado correctamente.")

if __name__ == "__main__":
    create_superuser()