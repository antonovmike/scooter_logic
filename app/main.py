import psycopg2
import time

from fastapi import FastAPI, Response, status
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from scooter.utils import ScooterStatus, scooter, client, employee


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', 
            password='123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        # If I set up wrong password start uvicorn app.main:app --reload
        # see this error, then change password to correct one I will still
        # in the loop. Even Ctrl+C doesn't help. But in the video this code
        # works fine: https://youtu.be/0sOvCWFmrtA?feature=shared&t=14803
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}


@app.get("/rent")
async def rent():
    scooter_status = client.take_scooter(scooter, scooter.is_available(False))
    print(scooter_status)
    return {"message": scooter_status}


@app.get("/service")
async def service():
    scooter_status = employee.take_scooter(scooter, scooter.is_available(True))
    print(scooter_status)
    return {"message": scooter_status}


@app.get("/free")
async def free():
    scooter_status = scooter.change_status(ScooterStatus.AVAILABLE)
    print(scooter_status)
    return {"message": scooter_status}
