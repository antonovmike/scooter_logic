import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.orm.declarative_base()


def get_db():
    """
    Provides a database session for each request.

    This function is a dependency that yields a database session. 
    It is designed to be used with FastAPI's dependency injection system, 
    allowing each request to have its own database session. 
    The session is automatically closed after the request is processed.

    Returns:
    - Session: A SQLAlchemy session object.

    Yields:
    - Session: The database session for the current request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
