from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

router = APIRouter()

from .. import models, utils
from app.database import get_db
from ..schemas import UserCreate, UserOut


router = APIRouter(
    prefix="/users",
    tags=['Users'] # Adds headers to documentation http://127.0.0.1:8000/redoc
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database with a hashed password.

    Parameters:
    - user (UserCreate): The user data to create, including a plaintext password.
    - db (Session): The database session.

    Returns:
    - UserOut: The created user object with the hashed password.
    """
    hashed_password: str = utils.hash(user.password)
    user.password = hashed_password

    new_user: models.User = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a user by its ID.

    Parameters:
    - id (int): The ID of the user to retrieve.
    - db (Session): The database session.

    Returns:
    - UserOut: The user object.

    Raises:
    - HTTPException: If the user with the given ID does not exist.
    """
    user: models.User = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id: {id} does not exist"
            )

    return user