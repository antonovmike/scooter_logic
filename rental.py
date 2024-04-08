from datetime import datetime

from logging_setup import log
from rental_system import RentalSystem
from scooter import ScooterStatus


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
            return RegularRental(scooter)
        elif rental_type == RentType.DISCOUNTED:
            return DiscountedRental(scooter)
        elif rental_type == RentType.SERVICED:
            return ServiceRental(scooter)
        else:
            raise ValueError("Invalid rental type")


class RegularRental(RentalSystem):
    def rent(self):
        self.scooter.change_status(ScooterStatus.RENTED)


class DiscountedRental(RentalSystem):
    def rent(self):
        self.scooter.change_status(ScooterStatus.RENTED)


class ServiceRental(RentalSystem):
    def rent(self):
        self.scooter.change_status(ScooterStatus.SERVICE)
