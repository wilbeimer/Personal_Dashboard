from app.models import User
from passlib.context import CryptContext
from app.schemas import UserCreate
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate) -> User:
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed_pw)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
