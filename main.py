from scooter.scooter import (
    Battery,
    Scooter,
    ScooterStatus,
    ScooterStatusChecker,
)

from scooter.user import Client, Employee

# Example Usage
scooter = Scooter(ScooterStatus.AVAILABLE)
client = Client()
employee = Employee()
status_checker = ScooterStatusChecker()

print("> Client rents a scooter")
client.take_scooter(scooter, scooter.is_available(False))
print("> Client tries to rent rented scooter")
client.take_scooter(scooter, scooter.is_available(False))

print("> Employee tries to service rented scooter")
employee.take_scooter(scooter, scooter.is_available(True))

print("> Termination of rent")
scooter.change_status(ScooterStatus.AVAILABLE)
print("> Client rents a scooter")
client.take_scooter(scooter, scooter.is_available(False))
print("> Termination of rent")
scooter.change_status(ScooterStatus.AVAILABLE)

print("> Employee services a scooter")
employee.take_scooter(scooter, scooter.is_available(True))
print("> Client tries to rent scooter while it is in services")
client.take_scooter(scooter, scooter.is_available(False))
