from fastapi import FastAPI, Response, status

from scooter.utils import ScooterStatus, scooter, client, employee


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rent a scooter!"}


@app.get("/rent")
async def rent():
    scooter_status = client.take_scooter(scooter, scooter.is_available(False))
    print(scooter_status)
    return {"message": scooter_status}
    # return JSONResponse(content={"message": "rented"})


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
