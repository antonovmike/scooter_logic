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

print("1", scooter.is_available())

client = Client()
employee = Employee()

# # Client rents a scooter
client.rent_scooter(scooter, scooter.is_available())
client.rent_scooter(scooter, scooter.is_available())

# # Employee services a scooter
employee.service_scooter(scooter, scooter.is_available())

# # Using the RentalSystem with different rental types
regular_rental = RegularRental(scooter)
discounted_rental = DiscountedRental(scooter)
service_rental = ServiceRental(scooter)

rental_system = RentalSystem(regular_rental)
rental_system.rent()

scooter = Scooter(ScooterStatus.RESERVED)
print("2", scooter.is_available())

rental_system = RentalSystem(discounted_rental)
rental_system.rent()

rental_system = RentalSystem(service_rental)
rental_system.rent()

scooter.change_status(ScooterStatus.AVAILABLE)
print("3", scooter.is_available())

status_checker = ScooterStatusChecker()
status_checker.check_status(scooter)
