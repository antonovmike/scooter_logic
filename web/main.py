from fastapi import FastAPI, Response, status

from scooter.utils import scooter, client, employee, status_checker


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}


@app.get("/rent", status_code=status.HTTP_204_NO_CONTENT)
async def root():
    client.take_scooter(scooter, scooter.is_available())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/service", status_code=status.HTTP_204_NO_CONTENT)
async def root():
    employee.take_scooter(scooter, scooter.is_available())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/free", status_code=status.HTTP_204_NO_CONTENT)
async def root():
    scooter # changes scooter status to "available"
    return Response(status_code=status.HTTP_204_NO_CONTENT)
