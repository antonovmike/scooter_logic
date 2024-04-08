from datetime import datetime

from scooter import ScooterStatus
from logging_setup import log


class RentType:
    REGULAR = "regular"
    DISCOUNTED = "discounted"
    SERVICED = "serviced"


class RentalManager:
    def __init__(self):
        self.logger = log

    def determine_rental_type(self, user_is_employee):
        current_hour = datetime.now().hour
        if user_is_employee:
            return RentType.SERVICED
        elif 6 <= current_hour < 18:
            return RentType.REGULAR
        else:
            return RentType.DISCOUNTED

    def create_rental_instance(self, rental_type, scooter):
        if rental_type == RentType.REGULAR:
            self.logger.info("===> REGULAR")
            return RegularRental(scooter)
        elif rental_type == RentType.DISCOUNTED:
            self.logger.info("===> DISCOUNTED")
            return DiscountedRental(scooter)
        elif rental_type == RentType.SERVICED:
            self.logger.info("===> SERVICED")
            return ServiceRental(scooter)
        else:
            raise ValueError("Invalid rental type")


# Liskov Substitution Principle
class Rental:
    def __init__(self, scooter):
        self.logger = log
        self.scooter = scooter


class RegularRental(Rental):
    def rent(self):
        self.logger.info("===> RegularRental")
        self.scooter.change_status(ScooterStatus.RENTED)


class DiscountedRental(Rental):
    def rent(self):
        self.logger.info("===> DiscountedRental")
        self.scooter.change_status(ScooterStatus.RENTED)


# Dependency Inversion Principle
class ServiceRental(Rental):
    def rent(self):
        self.logger.info("===> ServiceRental")
        self.scooter.change_status(ScooterStatus.SERVICE)
