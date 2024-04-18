from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Scooter
from scooter.scooter import Battery, ScooterStatus, Scooter as ScooterLogic, battery_crytical

router = APIRouter()

# from app import models
# from app.database import get_db
from scooter.utils import ScooterStatus, scooter, client, employee


router = APIRouter(
    prefix="/rent",
    tags=['Rent'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


class InvalidScooterStatusError(Exception):
    pass


@router.get("/rent/{scooter_id}")
async def rent(scooter_id: int, db: Session = Depends(get_db)):
    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    battery = Battery(level=scooter.battery_level)
    scooter_logic = ScooterLogic(scooter.status, battery)

    if scooter_logic.battery.get_level() <= battery_crytical:
        raise HTTPException(status_code=400, detail="Scooter battery level is too low to rent")

    try:
        scooter_logic.change_status(ScooterStatus.RENTED)
    except InvalidScooterStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))

    scooter.status = scooter_logic.status

    scooter.battery_level = scooter_logic.decrease_battery(11)

    db.commit()

    return {"message": f"Scooter {scooter_id} is now rented"}


@router.get("/service/{scooter_id}")
async def service(scooter_id: int, db: Session = Depends(get_db)):
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

    scooter.battery_level = scooter_logic.charge_battery()

    db.commit()

    return {"message": f"Scooter {scooter_id} is now in service"}

@router.get("/free/{scooter_id}")
async def free(scooter_id: int, db: Session = Depends(get_db)):
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
