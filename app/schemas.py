from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base user model.

    Attributes:
    - name (str): The name of the user.
    - email (EmailStr): The email address of the user.
    - password (str): The hashed password of the user.
    - is_user_employee (bool): Indicates whether the user is an employee.
    """
    name: str
    email: EmailStr
    password: str
    is_user_employee: bool = False
    is_employee_repairer: bool = False

class UserCreate(UserBase):
    """User creation model.

    Attributes:
    - password (str): The plaintext password of the user.
    """
    pass

class UserOut(UserBase):
    """
    User model with extra fields.

    Attributes:
    - id (int): The unique identifier for the user.
    - created_at (datetime): The timestamp when the user was created.
    """
    id: int
    created_at: datetime

    class Config:
        """Configuration for the UserOut model."""
        from_attributes = True


class ScooterBase(BaseModel):
    """
    Base scooter model.

    Attributes:
    - model (str): The model of the scooter.
    - status (str): The current status of the scooter.
    """
    model: str
    status: str

class ScooterCreate(ScooterBase):
    """
    Scooter creation model.

    Attributes:
    - battery_level (int): The current battery level of the scooter, default is 100.
    """
    pass

class ScooterOut(ScooterBase):
    """
    Represents the output model for a scooter, including its basic information and additional metadata.

    This class inherits from `ScooterBase` and adds two additional fields: `id` and `created_at`. 
    The `id` field represents the unique identifier of the scooter, while `created_at` 
    stores the timestamp of when the scooter was created.

    Attributes:
    - id (int): The unique identifier for the scooter.
    - created_at (datetime): The timestamp when the scooter was created.

    Inherits from:
    - ScooterBase: Provides the basic information about the scooter, such as its model and status.

    Configuration:
    - from_attributes (bool): Set to True to include attributes in the model's schema.
    """
    id: int
    created_at: datetime

    class Config:
        """Configuration for the ScooterOut model."""
        from_attributes = True

class ScooterUpdate(BaseModel):
    """
    Represents the update model for a scooter, allowing changes to its status.

    This class is used to update the status of a scooter. 
    It inherits from `BaseModel` and defines a single field `status` which is a string.

    Attributes:
    - status (str): The new status of the scooter.
    """
    status: str


class Token(BaseModel):
    """
    Represents the structure of an authentication token.

    This class is used to model the structure of an authentication token, 
    including the access token itself and the token type.

    Attributes:
    - access_token (str): The access token string.
    - token_type (str): The type of the token, typically "bearer".
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the data contained within an authentication token.

    This class is used to model the data that is encoded within an authentication token, 
    specifically the user ID.

    Attributes:
    - id (Optional[int]): The ID of the user associated with the token. Defaults to None.
    """
    id: Optional[int] = None
