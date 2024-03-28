from abc import ABC, abstractmethod
from datetime import datetime

from rental import Rental, RegularRental, DiscountedRental, ServiceRental, RentType
from logging_setup import log


class RentalSystem:
    def __init__(self, rental):
        self.rental = rental

    def rent(self):
        self.rental.rent()


class RentalManager:
    def __init__(self):
        self.logger = log

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
