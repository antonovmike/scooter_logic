from fastapi import FastAPI, Response, status

from scooter.utils import ScooterStatus, scooter, client, employee


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}


@app.get("/rent", status_code=status.HTTP_204_NO_CONTENT)
async def rent():
    scooter_status = client.take_scooter(scooter, scooter.is_available(False))
    print(scooter_status)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/service", status_code=status.HTTP_204_NO_CONTENT)
async def service():
    scooter_status = employee.take_scooter(scooter, scooter.is_available(True))
    print(scooter_status)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/free", status_code=status.HTTP_204_NO_CONTENT)
async def free():
    scooter_status = scooter.change_status(ScooterStatus.AVAILABLE)
    print(scooter_status)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
