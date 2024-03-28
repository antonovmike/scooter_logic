from abc import ABC, abstractmethod
from datetime import datetime

# from client import

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


# Liskov Substitution Principle
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
