from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

router = APIRouter()

from .. import models
from app.database import get_db
from ..schemas import ScooterCreate, ScooterOut, ScooterUpdate


router = APIRouter(
    prefix="/scooters",
    tags=['Scooters'] # Adds headers to documentation http://127.0.0.1:8000/redoc
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ScooterOut)
def create_scooter(scooter: ScooterCreate, db: Session = Depends(get_db)):
    new_scooter = models.Scooter(**scooter.model_dump())
    db.add(new_scooter)
    db.commit()
    db.refresh(new_scooter)

    return new_scooter


@router.get("/{id}", response_model=ScooterOut)
def get_scooter(id: int, db: Session = Depends(get_db)):
    scooter = db.query(models.Scooter).filter(models.Scooter.id == id).first()

    if not scooter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Scooter with id: {id} does not exist"
            )

    return scooter


@router.put("/{id}", response_model=ScooterOut)
def update_scooter_status(id: int, scooter_update: ScooterUpdate, db: Session = Depends(get_db)):
    scooter = db.query(models.Scooter).filter(models.Scooter.id == id).first()
    if not scooter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Scooter with id: {id} does not exist"
        )
    scooter.status = scooter_update.status
    db.commit()
    db.refresh(scooter)

    return scooter
