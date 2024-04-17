from datetime import datetime
from pydantic import BaseModel
# from typing import Optional


"""
Approximate database schema:
users (ID, is_user_employee, user_id)
employee (ID, name, phone)
customer (ID, name, phone)
scooter (ID, status)
logs (ID, action_date, action_type, user_id, scooter_id)
Customer and employee should be in different tables, as their data may differ. 
For example, an employee may have a position and a qualification level
"""

class UserBase(BaseModel):
    name: str
    phone: str
    password: str
    is_user_employee: bool = True

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    created_at: datetime

    class Config:
        from_attributes = True


class ScooterBase(BaseModel):
    model: str
    status: str

class ScooterCreate(ScooterBase):
    pass

class ScooterOut(ScooterBase):
    created_at: datetime

    class Config:
        from_attributes = True
