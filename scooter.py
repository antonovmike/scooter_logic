# encapsulate scooter's state and behavior
class Scooter:
    def __init__(self, status):
        self.status = status

    def change_status(self, new_status):
        self.status = new_status


# different types of users interacting with the scooter system
class Client:
    def rent_scooter(self, scooter):
        scooter.change_status("rented")


class Employee:
    def service_scooter(self, scooter):
        scooter.change_status("service")


# These classes will inherit from a common Rental base class,
# allowing them to be used interchangeably
class Rental:
    def __init__(self, scooter):
        self.scooter = scooter


class RegularRental(Rental):
    def rent(self):
        self.scooter.change_status("rented")


class DiscountedRental(Rental):
    def rent(self):
        self.scooter.change_status("rented")


# Interface for the rental system depends on abstractions (Rental)
# rather than concrete implementations.
class ServiceRental(Rental):
    def rent(self):
        self.scooter.change_status("service")


class RentalSystem:
    def __init__(self, rental):
        self.rental = rental

    def rent(self):
        self.rental.rent()
