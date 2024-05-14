from fastapi import FastAPI

from . import models
from .database import engine
from .routers import rout_rent, rout_scooters, rout_user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', 
#             password='123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         # If I set up wrong password start uvicorn app.main:app --reload
#         # see this error, then change password to correct one I will still
#         # in the loop. Even Ctrl+C doesn't help. But in the video this code
#         # works fine: https://youtu.be/0sOvCWFmrtA?feature=shared&t=14803
#         time.sleep(2)


app.include_router(rout_rent.router)
app.include_router(rout_user.router)
app.include_router(rout_scooters.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}
