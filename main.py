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

# print("> Using the RentalSystem with different rental types")
regular_rental = RegularRental(scooter)
discounted_rental = DiscountedRental(scooter)
service_rental = ServiceRental(scooter)

rental_system = RentalSystem(regular_rental)
rental_system.rent()

# print("> Client reserves scooter")
scooter = Scooter(ScooterStatus.RESERVED)
status_checker.check_status(scooter)

# print("> Discounted rental")
rental_system = RentalSystem(discounted_rental)
rental_system.rent()

# print("> Service rental")
rental_system = RentalSystem(service_rental)
rental_system.rent()

# print("> Termination of rent")
scooter.change_status(ScooterStatus.AVAILABLE)
# print("> Check status")
status_checker.check_status(scooter)
