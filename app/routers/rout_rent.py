from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import oauth2
from app.database import get_db
from app.models import Scooter, User
from scooter.scooter import Battery, ScooterStatus, Scooter as ScooterLogic, battery_crytical
from scooter.utils import ScooterStatus


router = APIRouter()


router = APIRouter(
    prefix="/rent",
    tags=['Rent'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


class InvalidScooterStatusError(Exception):
    pass


@router.get("/rent/{scooter_id}")
async def rent(scooter_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)

    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    battery = Battery(level=scooter.battery_level)

    employee = db.query(User).filter(User.id == user_id.id).first()

    if employee.is_user_employee:
        print("User is employee")
    else:
        print("User is customer")

    scooter_logic = ScooterLogic(scooter.status, battery)

    if scooter.status != ScooterStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail=f"Scooter is not available: {scooter.status}")

    if scooter_logic.battery.get_level() <= battery_crytical:
        raise HTTPException(status_code=400, detail="Scooter battery level is too low to rent")

    try:
        scooter_logic.change_status(ScooterStatus.RENTED)
    except InvalidScooterStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))

    scooter.status = scooter_logic.status

    scooter_logic.decrease_battery(17)
    scooter.battery_level = scooter_logic.battery.get_level()

    db.commit()

    return {"message": f"Scooter {scooter_id} is now rented"}


@router.get("/service/{scooter_id}")
async def service(scooter_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    employee = db.query(User).filter(User.id == user_id.id).first()

    if scooter.status != ScooterStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail=f"Scooter is not available: {scooter.status}")

    if employee.is_user_employee:
        scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
        if not scooter:
            raise HTTPException(status_code=404, detail="Scooter not found")

        battery = Battery(level=scooter.battery_level)
        scooter_logic = ScooterLogic(scooter.status, battery)

        try:
            scooter_logic.change_status(ScooterStatus.SERVICE)
        except InvalidScooterStatusError as e:
            raise HTTPException(status_code=400, detail=str(e))

        scooter.status = scooter_logic.status

        scooter_logic.charge_battery()
        scooter.battery_level = scooter_logic.battery.get_level()

        db.commit()

        return {"message": f"Scooter {scooter_id} is now in service"}
    else:
        return {"message": f"You are not an employee"}
    

@router.get("/free/{scooter_id}")
async def free(scooter_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)

    if scooter.status == ScooterStatus.LOST:
        raise HTTPException(status_code=400, detail=f"Impossible to change scooter's status: {scooter.status}")

    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
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
    db.commit()

    return {"message": f"Scooter {scooter_id} is available"}
