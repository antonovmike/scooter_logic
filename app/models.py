from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_user_employee = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, nullable=False)
    model = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)


class ScooterLog(Base):
    __tablename__ = "scooter_log"
    
    id = Column(Integer, primary_key=True, nullable=False)
    action_date= Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)
    action_type = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    scooter_id = Column(Integer, nullable=False)