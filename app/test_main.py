import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base, SQLALCHEMY_DATABASE_URL
from app import oauth2
from app.main import app
from app.models import Scooter, User
from scooter.scooter import ScooterStatus, Battery, Scooter as ScooterLogic

client = TestClient(app)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def test_scooter():
    """Creates a test scooter in the database."""
    db = SessionLocal()

    scooter = Scooter(model="TEST", status=ScooterStatus.AVAILABLE)

    db.add(scooter)
    db.commit()
    db.refresh(scooter)

    yield scooter

    db.delete(scooter)
    db.commit()
    db.close()

@pytest.fixture(scope="function")
def test_non_employee_user():
    """Creates a test non-employee user in the database."""
    db = SessionLocal()

    non_employee_user = User(id=44, name="customer", password="customer", email="customer", is_user_employee=False)
    db.add(non_employee_user)
    db.commit()
    db.refresh(non_employee_user)

    yield non_employee_user

    db.delete(non_employee_user)
    db.commit()
    db.close()

@pytest.fixture(scope="function")
def test_employee_user():
    """Creates a test employee user in the database."""
    db = SessionLocal()

    employee_user = User(id=55, name="employee", password="employee", email="employee", is_user_employee=True)
    db.add(employee_user)
    db.commit()
    db.refresh(employee_user)

    yield employee_user

    db.delete(employee_user)
    db.commit()
    db.close()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rent a scooter!"}


def test_rent(test_scooter, test_non_employee_user):
    non_employee_token = oauth2.create_access_token(data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/rent/{test_scooter.id}", headers={"Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now rented"}

def test_free(test_scooter, test_non_employee_user):
    non_employee_token = oauth2.create_access_token(data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/free/{test_scooter.id}", headers={"Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is available"}

def test_service(test_scooter, test_employee_user):
    empoyee_token = oauth2.create_access_token(data={"user_id": test_employee_user.id, "is_user_employee": True})
    response = client.get(f"/rent/service/{test_scooter.id}", headers={"Authorization": f"Bearer {empoyee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now in service"}

def test_service_non_employee(test_scooter, test_non_employee_user):
    """Tests that a non-employee user cannot service a scooter"""

    non_employee_token = oauth2.create_access_token(data={"user_id": test_non_employee_user.id, "is_user_employee": False})

    response = client.get(f"/rent/service/{test_scooter.id}", headers={"Authorization": f"Bearer {non_employee_token}"})

    assert response.status_code == 200
    assert response.json() == {"message": "You are not an employee"}

def test_user_status(test_non_employee_user, test_employee_user):
    assert test_non_employee_user.is_user_employee is False
    assert test_employee_user.is_user_employee is True

def test_low_battery_status(test_scooter, test_non_employee_user):
    test_scooter.battery_level = 10

    db = SessionLocal()
    db.query(Scooter).filter(Scooter.id == test_scooter.id).update({Scooter.battery_level: test_scooter.battery_level})
    db.commit()

    non_employee_token = oauth2.create_access_token(data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/free/{test_scooter.id}", headers={"Authorization": f"Bearer {non_employee_token}"})

    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id}: Low battery"}

def test_battery_below_zero(test_scooter, test_non_employee_user):
    scooter = ScooterLogic(status=ScooterStatus.AVAILABLE, battery=Battery(level=100))
    scooter.decrease_battery(110)
    assert scooter.get_battery_level() == 0
