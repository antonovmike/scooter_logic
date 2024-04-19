from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_user_employee: bool = True

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ScooterBase(BaseModel):
    model: str
    status: str

class ScooterCreate(ScooterBase):
    pass

class ScooterOut(ScooterBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ScooterUpdate(BaseModel):
    status: str
