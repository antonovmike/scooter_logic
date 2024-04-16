from fastapi.testclient import TestClient

from app.main import app
from scooter.scooter import ScooterStatus

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rent a scooter!"}


def test_rent():
    response = client.get("/rent/rent")
    assert response.status_code == 200
    assert response.json() == {"message": ScooterStatus.RENTED}


def test_free():
    response = client.get("/rent/free")
    assert response.status_code == 200
    assert response.json() == {"message": ScooterStatus.AVAILABLE}


def test_service():
    response = client.get("/rent/service")
    assert response.status_code == 200
    assert response.json() == {"message": ScooterStatus.SERVICE}
