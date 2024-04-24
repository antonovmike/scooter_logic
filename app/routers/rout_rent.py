from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import oauth2
from app.database import get_db
from app.models import Scooter, ScooterLog, User
from scooter.scooter import Battery, ScooterStatus, Scooter as ScooterLogic, battery_crytical
from scooter.utils import ScooterStatus


router = APIRouter(
    prefix="/rent",
    tags=['Rent'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


class InvalidScooterStatusError(Exception):
    pass


@router.get("/rent/{scooter_id}")
async def rent(scooter_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    scooter, scooter_logic = get_scooter_and_check_availability(db, scooter_id, current_user)

    if scooter_logic.battery.get_level() <= battery_crytical:
        raise HTTPException(status_code=400, detail="Scooter battery level is too low to rent")

    update_scooter_status_and_battery(db, scooter, scooter_logic, ScooterStatus.RENTED, current_user)

    return {"message": f"Scooter {scooter_id} is now rented"}


@router.get("/service/{scooter_id}")
async def service(
    scooter_id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
    ):
    scooter, scooter_logic = get_scooter_and_check_availability(db, scooter_id, current_user)

    if current_user.is_user_employee:
        update_scooter_status_and_battery(db, scooter, scooter_logic, ScooterStatus.SERVICE, current_user)
        return {"message": f"Scooter {scooter_id} is now in service"}
    else:
        return {"message": f"You are not an employee"}


@router.get("/free/{scooter_id}")
async def free(scooter_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.name)

    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()

    if scooter.status == ScooterStatus.LOST:
        raise HTTPException(status_code=400, detail=f"Impossible to change scooter's status: {scooter.status}")

    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    battery = Battery(level=scooter.battery_level)
    scooter_logic = ScooterLogic(scooter.status, battery)

    try:
        scooter_logic.change_status(ScooterStatus.AVAILABLE)
    except InvalidScooterStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))

    scooter.status = scooter_logic.status

    scooter.battery_level = scooter_logic.battery.get_level()

    add_to_scooter_log(db, scooter_id, scooter.status, current_user.id)

    db.commit()

    return {"message": f"Scooter {scooter_id} is available"}


def add_to_scooter_log(db: Session, scooter_id: int, action_type: str, user_id: int):
    scooter_log = ScooterLog(scooter_id=scooter_id, action_type=action_type, user_id=user_id)
    if not scooter_log:
        raise HTTPException(status_code=404, detail="Scooter log not found")
    else:
        db.add(scooter_log)
        db.commit()


def get_scooter_and_check_availability(db: Session, scooter_id: int, current_user: int):
    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    if scooter.status == ScooterStatus.LOST:
        raise HTTPException(status_code=400, detail=f"Impossible to change scooter's status: {scooter.status}")

    battery = Battery(level=scooter.battery_level)
    scooter_logic = ScooterLogic(scooter.status, battery)

    if not scooter_logic.is_available(current_user.is_user_employee):
        raise HTTPException(status_code=400, detail=f"Scooter is not available: {scooter.status}")

    return scooter, scooter_logic


def update_scooter_status_and_battery(
        db: Session, 
        scooter: Scooter, 
        scooter_logic: ScooterLogic, 
        new_status: ScooterStatus, 
        current_user, 
        battery_change: int = 0
        ):
    try:
        scooter_logic.change_status(new_status)
    except InvalidScooterStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))

    scooter.status = scooter_logic.status
    scooter_logic.decrease_battery(battery_change)
    scooter.battery_level = scooter_logic.battery.get_level()

    add_to_scooter_log(db, scooter.id, scooter.status, current_user.id)
    db.commit()
