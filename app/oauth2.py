from datetime import datetime, timedelta, UTC
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from sqlalchemy.orm import Session

from . import database, models, schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # Depends on router @router.post('/login')

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """
    Creates a new access token with an expiration time.

    Parameters:
    - data (dict): The data to be encoded into the token.

    Returns:
    - str: The encoded JWT access token.

    Raises:
    - None
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
    """
    Verifies the access token and extracts the user ID from it.

    Parameters:
    - token (str): The JWT token to verify.
    - credentials_exception (HTTPException): The exception to raise if verification fails.

    Returns:
    - schemas.TokenData: The token data containing the user ID.

    Raises:
    - HTTPException: If the token is invalid or the user ID is missing.
    """
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id") # Depends on app/routers/auth.py access_token = oauth2.create_access_token(data= {"user_id": user.id})

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Retrieves the current user based on the provided token.

    Parameters:
    - token (str): The JWT token to verify and extract the user ID.
    - db (Session): The database session.

    Returns:
    - models.User: The user object corresponding to the provided token.

    Raises:
    - HTTPException: If the token is invalid or the user ID is missing.
    """
    credentials_exception: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Could not validate credentians", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    token: str = verify_access_token(token, credentials_exception)

    user: models.User = db.query(models.User).filter(models.User.id == token.id).first()

    return user
