import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base, SQLALCHEMY_DATABASE_URL
from app import oauth2
from app.main import app
from app.models import Scooter
from scooter.scooter import ScooterStatus

client = TestClient(app)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
token = oauth2.create_access_token(data={"user_id": 1})

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def test_scooter():
    db = SessionLocal()

    scooter = Scooter(model="TEST", status=ScooterStatus.AVAILABLE)
    db.add(scooter)
    db.commit()
    db.refresh(scooter)

    yield scooter

    db.delete(scooter)
    db.commit()
    db.close()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rent a scooter!"}


def test_rent(test_scooter):
    response = client.get(f"/rent/rent/{test_scooter.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now rented"}


@pytest.fixture(scope="function")
def test_free(test_scooter):
    response = client.get(f"/rent/free/{test_scooter.id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is available"}


@pytest.fixture(scope="function")
def test_service(test_scooter):
    response = client.get(f"/rent/service/{test_scooter.id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now in service"}
