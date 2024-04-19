from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # default= and server_default= do not work
    is_user_employee = Column(Boolean, server_default=text('False'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, nullable=False)
    model = Column(String, nullable=False)
    status = Column(String, nullable=False)
    battery_level = Column(Integer, nullable=False, default=100)
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