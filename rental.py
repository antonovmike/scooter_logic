import logging

from abc import ABC, abstractmethod
from datetime import datetime

from scooter import ScooterStatus


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class RentType:
    REGULAR = "regular"
    DISCOUNTED = "discounted"


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
