from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rent a scooter!"}


def test_rent():
    response = client.get("/rent")
    assert response.status_code == 204


def test_service():
    response = client.get("/service")
    assert response.status_code == 204


def test_free():
    response = client.get("/free")
    assert response.status_code == 204
