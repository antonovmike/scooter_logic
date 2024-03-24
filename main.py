from scooter import (
    Scooter,
    Client,
    Employee,
    RegularRental,
    DiscountedRental,
    RentalSystem,
    ServiceRental,
    ScooterStatus,
)

# Example Usage
scooter = Scooter(ScooterStatus.AVAILABLE)
print(scooter.is_available())

client = Client()
employee = Employee()

# Client rents a scooter
client.rent_scooter(scooter)

# Employee services a scooter
employee.service_scooter(scooter)

# Using the RentalSystem with different rental types
regular_rental = RegularRental(scooter)
discounted_rental = DiscountedRental(scooter)
service_rental = ServiceRental(scooter)

rental_system = RentalSystem(regular_rental)
rental_system.rent()

scooter = Scooter(ScooterStatus.RESERVED)
print(scooter.is_available())

rental_system = RentalSystem(discounted_rental)
rental_system.rent()

rental_system = RentalSystem(service_rental)
rental_system.rent()

scooter.change_status(ScooterStatus.AVAILABLE)
print(scooter.is_available())
