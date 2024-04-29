from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    """
    Represents a user in the system.

    Attributes:
    - id (int): The unique identifier for the user.
    - name (str): The name of the user.
    - email (str): The email address of the user.
    - password (str): The hashed password of the user.
    - is_user_employee (bool): Indicates whether the user is an employee.
    - created_at (TIMESTAMP): The timestamp when the user was created.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_user_employee = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)


class Scooter(Base):
    """
    Represents a scooter in the system.

    Attributes:
    - id (int): The unique identifier for the scooter.
    - model (str): The model of the scooter.
    - status (str): The current status of the scooter.
    - battery_level (int): The current battery level of the scooter, default is 100.
    - created_at (TIMESTAMP): The timestamp when the scooter was created.
    """
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, nullable=False)
    model = Column(String, nullable=False)
    status = Column(String, nullable=False)
    battery_level = Column(Integer, nullable=False, default=100)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)


class ScooterLog(Base):
    """
    Represents a log entry for a scooter action.

    Attributes:
    - id (int): The unique identifier for the log entry.
    - action_date (TIMESTAMP): The timestamp of the action.
    - action_type (str): The type of action performed on the scooter.
    - user_id (int): The ID of the user who performed the action.
    - scooter_id (int): The ID of the scooter on which the action was performed.
    """
    __tablename__ = "scooter_log"
    
    id = Column(Integer, primary_key=True, nullable=False)
    action_date= Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)
    action_type = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    scooter_id = Column(Integer, nullable=False)