from fastapi import APIRouter
# from sqlalchemy.orm import Session

router = APIRouter()

# from app import models
# from app.database import get_db
from scooter.utils import ScooterStatus, scooter, client, employee


router = APIRouter(
    prefix="/rent",
    tags=['Rent'] # Adds headers to documentation http://127.0.0.1:8000/docs
)


@router.get("/rent")
async def rent():
    scooter_status = client.take_scooter(scooter, scooter.is_available(False))
    print(scooter_status)
    return {"message": scooter_status}


@router.get("/service")
async def service():
    scooter_status = employee.take_scooter(scooter, scooter.is_available(True))
    print(scooter_status)
    return {"message": scooter_status}


@router.get("/free")
async def free():
    scooter_status = scooter.change_status(ScooterStatus.AVAILABLE)
    print(scooter_status)
    return {"message": scooter_status}
