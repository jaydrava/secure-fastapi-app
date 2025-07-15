from pydantic import BaseModel, EmailStr, SecretStr
from datetime import datetime


# ------- Input Schemas -------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr  # Use SecretStr for sensitive data


# ------- Output Schemas -------
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }  # Allows Pydantic to read data from ORM models
    # model_config = {"orm_mode": True}  # Alternative way to set ORM mode
