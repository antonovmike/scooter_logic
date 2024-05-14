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

    non_employee_user = User(id=44, name="customer", password="customer", email="customer")
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

    employee_user = User(id=55, name="employee", 
        password="employee", email="employee", is_user_employee=True)
    db.add(employee_user)
    db.commit()
    db.refresh(employee_user)

    yield employee_user

    db.delete(employee_user)
    db.commit()
    db.close()

@pytest.fixture(scope="function")
def test_repairer_user():
    """Creates a test repairer user in the database."""
    db = SessionLocal()

    repairer_user = User(id=66, name="repairer", password="repairer", 
        email="repairer", is_user_employee=True, is_employee_repairer=True)
    db.add(repairer_user)
    db.commit()
    db.refresh(repairer_user)

    yield repairer_user

    db.delete(repairer_user)
    db.commit()
    db.close()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rent a scooter!"}


def test_rent(test_scooter, test_non_employee_user):
    non_employee_token = oauth2.create_access_token(
        data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/rent/{test_scooter.id}", headers={
        "Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now rented"}

def test_free(test_scooter, test_non_employee_user):
    non_employee_token = oauth2.create_access_token(
        data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/free/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is available"}

def test_service(test_scooter, test_employee_user):
    empoyee_token = oauth2.create_access_token(
        data={"user_id": test_employee_user.id, "is_user_employee": True})
    response = client.get(f"/rent/service/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {empoyee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now in service"}

def test_repair_not_malfunction(test_scooter, test_repairer_user):
    empoyee_token = oauth2.create_access_token(
        data={"user_id": test_repairer_user.id, "is_employee_repairer": True})
    response = client.get(f"/rent/repair/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {empoyee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is not in malfunction"}

def test_repair_malfunction(test_scooter, test_repairer_user):
    """Tests the case when scooter is MALFUNCTION"""
    battery = Battery(level=100)
    scooter_logic = ScooterLogic(status=test_scooter.status, battery=battery)

    scooter_logic.change_status(ScooterStatus.MALFUNCTION)
    db = SessionLocal()
    db_scooter = db.query(Scooter).filter(Scooter.id == test_scooter.id).first()
    db_scooter.status = ScooterStatus.MALFUNCTION
    db.commit()

    empoyee_token = oauth2.create_access_token(
        data={"user_id": test_repairer_user.id, "is_employee_repairer": True})
    response = client.get(f"/rent/repair/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {empoyee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now in available"}


def test_rent_unauthorized_user(test_scooter):
    response = client.get(f"/rent/rent/{test_scooter.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_service_non_employee(test_scooter, test_non_employee_user):
    """Tests that a non-employee user cannot service a scooter"""

    non_employee_token = oauth2.create_access_token(
        data={"user_id": test_non_employee_user.id, "is_user_employee": False})

    response = client.get(f"/rent/service/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {non_employee_token}"})

    assert response.status_code == 200
    assert response.json() == {"message": "You are not an employee"}

def test_user_status(test_non_employee_user, test_employee_user):
    assert test_non_employee_user.is_user_employee is False
    assert test_employee_user.is_user_employee is True

def test_low_battery_status(test_scooter, test_non_employee_user):
    test_scooter.battery_level = 10

    db = SessionLocal()
    db.query(Scooter).filter(Scooter.id == test_scooter.id).update(
        {Scooter.battery_level: test_scooter.battery_level})
    db.commit()

    non_employee_token = oauth2.create_access_token(
        data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/free/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {non_employee_token}"})

    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id}: Low battery"}

def test_battery_below_zero():
    scooter = ScooterLogic(status=ScooterStatus.AVAILABLE, battery=Battery(level=100))
    scooter.decrease_battery(110)
    assert scooter.get_battery_level() == 0


def test_rent_already_rented_scooter(test_scooter, test_non_employee_user):
    non_employee_token = oauth2.create_access_token(
        data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get(f"/rent/rent/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now rented"}

    response = client.get(f"/rent/rent/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 400
    assert response.json() == {"detail": f"Scooter is not available"}

def test_rent_nonexistent_scooter(test_non_employee_user):
    non_employee_token = oauth2.create_access_token(
        data={"user_id": test_non_employee_user.id, "is_user_employee": False})
    response = client.get("/rent/rent/9999", 
        headers={"Authorization": f"Bearer {non_employee_token}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Scooter not found"}

def test_update_scooter_status_and_battery(test_scooter, test_employee_user):
    employee_token = oauth2.create_access_token(
        data={"user_id": test_employee_user.id, "is_user_employee": True})

    initial_status = test_scooter.status

    response = client.get(f"/rent/service/{test_scooter.id}", 
        headers={"Authorization": f"Bearer {employee_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": f"Scooter {test_scooter.id} is now in service"}

    db = SessionLocal()

    update_scooter = db.query(Scooter).filter(Scooter.id == test_scooter.id).first()

    assert update_scooter.status != initial_status
    assert update_scooter.battery_level == 100
