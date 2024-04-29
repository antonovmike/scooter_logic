from datetime import datetime, timedelta, UTC
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from sqlalchemy.orm import Session

from . import database, models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # Depends on router @router.post('/login')

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "a4e3563f88551adc11724ca01168cbd99d543f31480879059be0253590f3ec69"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
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
    credentials_exception: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Could not validate credentians", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    token: str = verify_access_token(token, credentials_exception)

    user: models.User = db.query(models.User).filter(models.User.id == token.id).first()

    return user
