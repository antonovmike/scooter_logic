from abc import ABC, abstractmethod

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Single Responsibility Principle
# It handles the scooter’s status and encapsulates scooter's state and behavior
class Scooter:
    def __init__(self, status):
        self.status = status
        self.logger = logging.getLogger(__name__)

    def change_status(self, new_status):
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")


class ScooterStatus:
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    LOW_BATTERY = "low battery"
    MALFUNCTION = "malfunction"
    SERVICE = "service"
    LOST = "lost"


# Interface Segregation Principle
# Different types of users interacting with the scooter system
class ClientInterface(ABC):
    @abstractmethod
    def rent_scooter(self, scooter):
        """Rent a scooter."""
        pass


class EmployeeInterface(ABC):
    @abstractmethod
    def service_scooter(self, scooter):
        """Service a scooter."""
        pass


class Client(ClientInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def rent_scooter(self, scooter):
        scooter.change_status("rented")
        self.logger.info("Scooter rented by client")


class Employee(EmployeeInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def service_scooter(self, scooter):
        scooter.change_status("service")
        self.logger.info("Scooter serviced by employee")


# Liskov Substitution Principle
# These classes will inherit from a common Rental base class,
# allowing them to be used interchangeably
class Rental:
    def __init__(self, scooter):
        self.scooter = scooter


class RegularRental(Rental):
    def rent(self):
        self.scooter.change_status(ScooterStatus.RENTED)


class DiscountedRental(Rental):
    def rent(self):
        self.scooter.change_status(ScooterStatus.RENTED)


# Dependency Inversion Principle
# Interface for the rental system depends on abstractions (Rental)
# rather than concrete implementations.
# This allows us to easily swap out rental types without
# modifying the client or employee classes.
class ServiceRental(Rental):
    def rent(self):
        self.scooter.change_status(ScooterStatus.SERVICE)


class RentalSystem:
    def __init__(self, rental):
        self.rental = rental

    def rent(self):
        self.rental.rent()
