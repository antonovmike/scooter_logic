from scooter import (
    Scooter,
    ScooterStatus,
    ScooterStatusChecker,
)

from client import Client, Employee

# Example Usage
scooter = Scooter(ScooterStatus.AVAILABLE)
client = Client()
employee = Employee()
status_checker = ScooterStatusChecker()

# print("> Client rents a scooter")
client.take_scooter(scooter, scooter.is_available())
# print("> Client tries to rent rented scooter")
client.take_scooter(scooter, scooter.is_available())

# print("> Employee tries to service rented scooter")
employee.take_scooter(scooter, scooter.is_available())

# print("> Termination of rent")
scooter.change_status(ScooterStatus.AVAILABLE)

# print("> Employee services a scooter")
employee.take_scooter(scooter, scooter.is_available())
print("Client tries to rent scooter while it is in services")
client.take_scooter(scooter, scooter.is_available())
