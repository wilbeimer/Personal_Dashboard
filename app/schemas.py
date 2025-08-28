from pydantic import BaseModel, EmailStr, PositiveInt, constr
from datetime import datetime

# Base model with global config


class StrictBaseModel(BaseModel):
    model_config = {"extra": "forbid"}  # No extra fields allowed anywhere


class UserCreate(StrictBaseModel):
    email: EmailStr
    password: constr(min_length=1, max_length=100)


class UserOut(StrictBaseModel):
    id: PositiveInt
    email: EmailStr


class NoteCreate(StrictBaseModel):
    title: constr(min_length=1, max_length=255)
    content: constr(max_length=255)


class NoteOut(StrictBaseModel):
    id: int
    user_id: int
    title: constr(min_length=1, max_length=255)
    content: constr(max_length=255)
    created_at: datetime
    updated_at: datetime
