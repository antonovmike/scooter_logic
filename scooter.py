from abc import ABC, abstractmethod
from datetime import datetime

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class InvalidScooterStatusError(Exception):
    """Raised when an invalid scooter status is attempted to be set."""

    pass


# Single Responsibility Principle
class Scooter:
    def __init__(self, status):
        self.status = status
        self.logger = logging.getLogger(__name__)

    def change_status(self, new_status):
        if new_status not in ScooterStatus.__dict__.values():
            raise InvalidScooterStatusError(f"Invalid status: {new_status}")
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


class RentType:
    REGULAR = "regular"
    DISCOUNTED = "discounted"


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


class RentalManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def determine_rental_type(self):
        current_hour = datetime.now().hour
        if 6 <= current_hour < 18:
            return RentType.REGULAR
        else:
            return RentType.DISCOUNTED

    def create_rental_instance(self, rental_type, scooter):
        if rental_type == RentType.REGULAR:
            return RegularRental(scooter)
        elif rental_type == RentType.DISCOUNTED:
            return DiscountedRental(scooter)
        else:
            raise ValueError("Invalid rental type")


class Client(ClientInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rental_manager = RentalManager()

    def rent_scooter(self, scooter, status_checker):
        try:
            if status_checker:
                # Use RentalManager to determine the rental type and create the Rental instance
                rental_type = self.rental_manager.determine_rental_type()
                rental = self.rental_manager.create_rental_instance(
                    rental_type, scooter
                )
                # Use the Rental instance to rent the scooter
                rental.rent()
                self.logger.info("Scooter rented by client")
            else:
                self.logger.error(f"Scooter is unavailable for rent: {scooter.status}")
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")


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
class ServiceRental(Rental):
    def rent(self):
        self.scooter.change_status(ScooterStatus.SERVICE)


class RentalSystem:
    def __init__(self, rental):
        self.rental = rental

    def rent(self):
        self.rental.rent()
