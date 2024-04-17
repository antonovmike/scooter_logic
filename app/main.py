import psycopg2
import time

from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import rent_router, user


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


app.include_router(rent_router.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}
