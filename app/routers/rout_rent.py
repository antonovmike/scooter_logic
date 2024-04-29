from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import oauth2
from app.database import get_db
from app.models import Scooter, ScooterLog, User
from logging_setup import log
from scooter.scooter import Battery, ScooterStatus, Scooter as ScooterLogic
from scooter.utils import ScooterStatus


router = APIRouter(
    prefix="/rent",
    tags=['Rent'] # Documentation header http://127.0.0.1:8000/docs
)


class InvalidScooterStatusError(Exception):
    """Exception raised when an invalid scooter status is encountered."""
    error = "Invalid scooter status"


@router.get("/rent/{scooter_id}")
async def rent(scooter_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Rents a scooter by updating its status and battery level.

    Parameters:
    - scooter_id (int): The ID of the scooter to rent.
    - db (Session): The database session.
    - current_user (int): The ID of the current user.

    Returns:
    - dict: A message indicating the scooter is now rented.

    Raises:
    - HTTPException: If the scooter battery level is too low or if the scooter is not available.
    """
    scooter, scooter_logic = get_scooter_and_check_availability(db, scooter_id, current_user)

    if scooter_logic.battery.get_level() <= scooter_logic.battery.battery_low(scooter_logic.battery.get_level()):
        raise HTTPException(status_code=400, detail="Scooter battery level is too low to rent")

    update_scooter_status_and_battery(db, scooter, scooter_logic, ScooterStatus.RENTED, current_user)

    return {"message": f"Scooter {scooter_id} is now rented"}


@router.get("/service/{scooter_id}")
async def service(
    scooter_id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
    ):
    """
    Services a scooter by updating its status.

    Parameters:
    - scooter_id (int): The ID of the scooter to service.
    - db (Session): The database session.
    - current_user (int): The ID of the current user.

    Returns:
    - dict: A message indicating the scooter is now in service or if the user is not an employee.

    Raises:
    - HTTPException: If the scooter is not available or if the user is not an employee.
    """
    scooter, scooter_logic = get_scooter_and_check_availability(db, scooter_id, current_user)

    user_status = db.query(User).filter(User.id == current_user.id).first().is_user_employee

    if user_status:
        if scooter.status == ScooterStatus.SERVICE:
            return {"message": f"Scooter {scooter_id} is already in service"}
        else:
            # Updates Scooter log only
            update_scooter_status_and_battery(db, scooter, scooter_logic, ScooterStatus.SERVICE, current_user)
            scooter.status = ScooterStatus.SERVICE
            scooter.battery_level = 100
            db.commit()
            return {"message": f"Scooter {scooter_id} is now in service"}
    else:
        return {"message": f"You are not an employee"}


@router.get("/free/{scooter_id}")
async def free(scooter_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Frees a scooter by updating its status to available.

    Parameters:
    - scooter_id (int): The ID of the scooter to free.
    - db (Session): The database session.
    - current_user (int): The ID of the current user.

    Returns:
    - dict: A message indicating the scooter is now available.

    Raises:
    - HTTPException: If the scooter is not found or if its status cannot be changed.
    """
    scooter: Scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()

    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    if scooter.status == ScooterStatus.LOST:
        raise HTTPException(status_code=400, detail=f"Impossible to change scooter's status: {scooter.status}")

    if Battery.battery_low(scooter.battery_level):
        scooter.status = ScooterStatus.LOW_BATTERY
        db.commit()
        return {"message": f"Scooter {scooter_id}: Low battery"}
    else:
        scooter.status = ScooterStatus.AVAILABLE
    db.commit()

    add_to_scooter_log(db, scooter_id, scooter.status, current_user.id)

    return {"message": f"Scooter {scooter_id} is available"}


def add_to_scooter_log(db: Session, scooter_id: int, action_type: str, user_id: int):
    """
    Adds an entry to the scooter log.

    Parameters:
    - db (Session): The database session.
    - scooter_id (int): The ID of the scooter.
    - action_type (str): The type of action performed on the scooter.
    - user_id (int): The ID of the user performing the action.

    Raises:
    - HTTPException: If the scooter log entry cannot be found.
    """
    scooter_log = ScooterLog(scooter_id=scooter_id, action_type=action_type, user_id=user_id)
    if not scooter_log:
        raise HTTPException(status_code=404, detail="Scooter log not found")
    else:
        db.add(scooter_log)
        db.commit()


def get_scooter_and_check_availability(db: Session, scooter_id: int, current_user: int):
    """
    Retrieves a scooter and checks its availability.

    Parameters:
    - db (Session): The database session.
    - scooter_id (int): The ID of the scooter.
    - current_user (int): The ID of the current user.

    Returns:
    - tuple: A tuple containing the scooter and its logic object.

    Raises:
    - HTTPException: If the scooter is not found, if its status is lost, or if it is not available.
    """
    scooter: Scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()

    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    battery = Battery(level=scooter.battery_level)
    scooter_logic: ScooterLogic = ScooterLogic(scooter.status, battery)

    if not scooter_logic.is_available(scooter):
        raise HTTPException(status_code=400, detail=f"Scooter is not available")

    return scooter, scooter_logic


def update_scooter_status_and_battery(
        db: Session, 
        scooter: Scooter, 
        scooter_logic: ScooterLogic, 
        new_status: ScooterStatus, 
        current_user: int, 
        battery_change: int = 20
        ):
    """
    Updates the status and battery level of a scooter.

    Parameters:
    - db (Session): The database session.
    - scooter (Scooter): The scooter object to update.
    - scooter_logic (ScooterLogic): The logic object for the scooter.
    - new_status (ScooterStatus): The new status for the scooter.
    - current_user (int): The ID of the current user.
    - battery_change (int): The change in battery level (default is 0).

    Raises:
    - HTTPException: If the new status is invalid.
    """
    try:
        scooter_logic.change_status(new_status)
    except InvalidScooterStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))

    scooter.status = scooter_logic.status
    scooter_logic.decrease_battery(battery_change)
    scooter.battery_level = scooter_logic.battery.get_level()

    add_to_scooter_log(db, scooter.id, scooter.status, current_user.id)
    db.commit()
