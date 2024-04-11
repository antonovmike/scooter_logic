from fastapi import FastAPI, Response, status

from scooter.utils import ScooterStatus, scooter, client, employee


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}


@app.get("/rent", status_code=status.HTTP_204_NO_CONTENT)
async def rent():
    client.take_scooter(scooter, scooter.is_available(False))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/service", status_code=status.HTTP_204_NO_CONTENT)
async def service():
    employee.take_scooter(scooter, scooter.is_available(True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/free", status_code=status.HTTP_204_NO_CONTENT)
async def free():
    scooter.change_status(ScooterStatus.AVAILABLE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
