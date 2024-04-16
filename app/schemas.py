from datetime import datetime
from pydantic import BaseModel


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
    id: int
    is_user_employee: bool = True
    user_id: int

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeModel(UserBase):
    id: int
    name: str
    phone: str
    date: datetime


class CustomerModel(UserBase):
    id: int
    name: str
    phone: str
    date: datetime


class VehicleBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ScooterModel(VehicleBase):
    status: str


class ScooterLogModel(BaseModel):
    id: int
    action_date: datetime
    action_type: str
    user_id: int
    scooter_id: int

    class Config:
        orm_mode = True
