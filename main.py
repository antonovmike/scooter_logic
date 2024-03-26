from scooter import (
    Scooter,
    Client,
    Employee,
    RegularRental,
    DiscountedRental,
    RentalSystem,
    ServiceRental,
    ScooterStatus,
    ScooterStatusChecker,
)

# Example Usage
scooter = Scooter(ScooterStatus.AVAILABLE)
client = Client()
employee = Employee()
status_checker = ScooterStatusChecker()

# print("> Client rents a scooter")
client.rent_scooter(scooter, scooter.is_available())
# print("> Client tries to rent rented scooter")
client.rent_scooter(scooter, scooter.is_available())

# print("> Employee tries to service rented scooter")
employee.service_scooter(scooter, scooter.is_available())

# print("> Termination of rent")
scooter.change_status(ScooterStatus.AVAILABLE)

# print("> Employee services a scooter")
employee.service_scooter(scooter, scooter.is_available())
print("Client tries to rent scooter while it is in services")
client.rent_scooter(scooter, scooter.is_available())
