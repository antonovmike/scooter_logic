import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123@localhost/scooters'

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
