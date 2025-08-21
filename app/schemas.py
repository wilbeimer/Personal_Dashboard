from pydantic import BaseModel, EmailStr, PositiveInt, constr

# Base model with global config


class StrictBaseModel(BaseModel):
    model_config = {"extra": "forbid"}  # No extra fields allowed anywhere


class UserCreate(StrictBaseModel):
    email: EmailStr
    password: constr(min_length=1, max_length=100)


class UserOut(StrictBaseModel):
    id: PositiveInt
    email: EmailStr
