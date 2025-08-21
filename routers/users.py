from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth import decode_access_token  # function to decode JWT
from app.auth import create_access_token
from app.crud import create_user, get_user_by_email
from app.database import get_db
from app.schemas import UserCreate, UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["users"])



@router.get("/", status_code=200)
def root():
    return {"status": "ok"}


@router.post("/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user_in)
    return new_user


@router.post("/login", status_code=200)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)

    if not user or not pwd_context.verify(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token({"sub": user.email})
    return {"access token": token, "token_type": "bearer"}


@router.post("/logout", status_code=200)
def logout():
    # Just a signal to the client
    return {"msg": "Logged out. Delete your token on the client side."}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


@router.get("/me", response_model=UserOut)
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
