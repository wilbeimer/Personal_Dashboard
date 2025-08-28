from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user
from app.crud import create_user, delete_all_users, get_user_by_email
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


@router.post("/login")
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)
    if not user or not pwd_context.verify(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    # Create a response that sets the cookie
    response = JSONResponse(
        content={"success": True, "access_token": token, "redirect": "/home"}
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Prevent JavaScript access
        secure=True,  # Only send over HTTPS
        samesite="lax",  # Protect against CSRF
    )
    return response


@router.post("/logout", status_code=200)
def logout():
    response = JSONResponse({"msg": "Logged out"})
    response.delete_cookie("access_token")
    return response


@router.delete("/delete_all", status_code=204)
def delete_all(db: Session = Depends(get_db)):
    delete_all_users(db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


@router.get("/me", response_model=UserOut)
def read_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
