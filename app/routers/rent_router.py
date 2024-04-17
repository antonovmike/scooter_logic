from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Scooter
from app.routers.scooters import update_scooter_status
from app.schemas import ScooterUpdate
from scooter.scooter import ScooterStatus

router = APIRouter()

# from app import models
# from app.database import get_db
from scooter.utils import ScooterStatus, scooter, client, employee


router = APIRouter(
    prefix="/rent",
    tags=['Rent'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


@router.get("/rent/{scooter_id}")
async def rent(scooter_id: int, db: Session = Depends(get_db)):
    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    if scooter.status != ScooterStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="Scooter is not available for rent")

    scooter.status = ScooterStatus.RENTED
    db.commit()

    return {"message": f"Scooter {scooter_id} is now rented"}


@router.get("/service/{scooter_id}")
async def service(scooter_id: int, db: Session = Depends(get_db)):
    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    if scooter.status != ScooterStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="Scooter is not available for service")

    scooter.status = ScooterStatus.SERVICE
    db.commit()

    return {"message": f"Scooter {scooter_id} is now in service"}


@router.get("/free/{scooter_id}")
async def free(scooter_id: int, db: Session = Depends(get_db)):
    scooter = db.query(Scooter).filter(Scooter.id == scooter_id).first()
    if not scooter:
        raise HTTPException(status_code=404, detail="Scooter not found")

    scooter.status = ScooterStatus.AVAILABLE
    db.commit()

    return {"message": f"Scooter {scooter_id} is available"}
