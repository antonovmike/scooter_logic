# Import "fastapi" could not be resolved PylancereportMissingImports
from fastapi import FastAPI, Response, status # type: ignore

from scooter.utils import ScooterStatus, scooter, client, employee, status_checker


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}


@app.get("/rent", status_code=status.HTTP_204_NO_CONTENT)
async def rent():
    client.take_scooter(scooter, scooter.is_available())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/service", status_code=status.HTTP_204_NO_CONTENT)
async def service():
    employee.take_scooter(scooter, scooter.is_available())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/free", status_code=status.HTTP_204_NO_CONTENT)
async def free():
    if scooter.status == ScooterStatus.LOW_BATTERY:
        print(f"Unavailable to rent, battery level is too low: {scooter.battery_level}")
    else:
        scooter.change_status(ScooterStatus.AVAILABLE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
