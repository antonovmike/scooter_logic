from abc import ABC, abstractmethod

import logging

# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


# Single Responsibility Principle
# It handles the scooter’s status and encapsulates scooter's state and behavior
class Scooter:
    def __init__(self, status):
        self.status = status
        self.logger = logging.getLogger(__name__)

    def change_status(self, new_status):
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")

    def is_available(self):
        return self.status == ScooterStatus.AVAILABLE


class ScooterStatus:
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    LOW_BATTERY = "low battery"
    MALFUNCTION = "malfunction"
    SERVICE = "service"
    LOST = "lost"


# Dependency Inversion Principle
class CurrentStatus(ABC):
    @abstractmethod
    def check_status(self, scooter):
        pass


class ScooterStatusChecker(CurrentStatus):
    def check_status(self, scooter):
        current_status = scooter.status
        scooter.logger.info(f"Scooter status is {current_status}")
        return current_status


# Interface Segregation Principle
# Different types of users interacting with the scooter system
class ClientInterface(ABC):
    @abstractmethod
    def rent_scooter(self, scooter, status_checker):
        """Rent a scooter."""
        pass


class EmployeeInterface(ABC):
    @abstractmethod
    def service_scooter(self, scooter, status_checker):
        """Service a scooter."""
        pass


class Client(ClientInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def rent_scooter(self, scooter, status_checker):
        if status_checker:
            scooter.change_status(ScooterStatus.RENTED)
            self.logger.info("Scooter rented by client")
        else:
            self.logger.error(f"Scooter is unavailable for rent: {scooter.status}")


class Employee(EmployeeInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def service_scooter(self, scooter, status_checker):
        if status_checker:
            scooter.change_status("service")
            self.logger.info("Scooter serviced by employee")
        else:
            self.logger.error(f"Unawailable for service: {scooter.status}")


# Liskov Substitution Principle
# These classes will inherit from a common Rental base class, allowing them to be used interchangeably
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
# Interface for the rental system depends on abstractions (Rental) rather than concrete implementations.
# This allows us to easily swap out rental types without modifying the client or employee classes.
class ServiceRental(Rental):
    def rent(self):
        self.scooter.change_status(ScooterStatus.SERVICE)


class RentalSystem:
    def __init__(self, rental):
        self.rental = rental

    def rent(self):
        self.rental.rent()
