from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .database import Base
from app.main import app
from app.models import Scooter
from scooter.scooter import ScooterStatus

client = TestClient(app)


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/scooters"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def create_scooter(model: str, status: str, db: Session):
    scooter = Scooter(model=model, status=status)
    db.add(scooter)
    db.commit()
    db.refresh(scooter)
    return scooter

db = SessionLocal()

scooter = create_scooter("TEST", ScooterStatus.AVAILABLE, db)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rent a scooter!"}


def test_rent():
    response = client.get(f"/rent/rent/{scooter.id}")
    assert response.status_code == 200
    # assert response.json() == {"message": ScooterStatus.RENTED}
    assert response.json() == {"message": f"Scooter {scooter.id} is now rented"}


def test_free():
    response = client.get(f"/rent/free/{scooter.id}")
    assert response.status_code == 200
    # assert response.json() == {"message": ScooterStatus.AVAILABLE}
    assert response.json() == {"message": f"Scooter {scooter.id} is available"}


def test_service():
    response = client.get(f"/rent/service/{scooter.id}")
    assert response.status_code == 200
    # assert response.json() == {"message": ScooterStatus.SERVICE}
    assert response.json() == {"message": f"Scooter {scooter.id} is now in service"}
