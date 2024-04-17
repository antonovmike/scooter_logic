from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.scooters import update_scooter_status
from app.schemas import ScooterUpdate

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

    scooter_update = ScooterUpdate(status="rented")
    update_scooter_status(scooter_id, scooter_update, db)

    return {"message": f"Scooter {scooter_id} is now rented"}

@router.get("/service/{scooter_id}")
async def service(scooter_id: int, db: Session = Depends(get_db)):

    scooter_update = ScooterUpdate(status="service")
    update_scooter_status(scooter_id, scooter_update, db)

    return {"message": f"Scooter {scooter_id} is now in service"}

@router.get("/free/{scooter_id}")
async def free(scooter_id: int, db: Session = Depends(get_db)):

    scooter_update = ScooterUpdate(status="available")
    update_scooter_status(scooter_id, scooter_update, db)

    return {"message": f"Scooter {scooter_id} is now available"}
