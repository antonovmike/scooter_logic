from abc import ABC, abstractmethod

from rental_system import RentalSystem
from logging_setup import log


class UserInterface(ABC):
    @abstractmethod
    def take_scooter(self, scooter, status_checker):
        """Blocks the ability to rent or service"""
        pass

    def _take_scooter(self, scooter, status_checker, rental_type, action_description):
        try:
            if status_checker and scooter.is_available():
                rental = self.rental_system.create_rental_instance(rental_type, scooter)
                rental.rent()
                self.logger.info(action_description)
                return True
            else:
                self.logger.error(f"Scooter is unavailable for rent: {scooter.status}")
                return False
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")
            return False


class Client(UserInterface):
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log

    def take_scooter(self, scooter, status_checker):
        if scooter.battery() > 20:
            rental_type = self.rental_system.determine_rental_type(user_is_employee=False)
            if self._take_scooter(scooter, status_checker, rental_type, "Scooter rented by client"):
                scooter.decrease_battery(15)
        else:
            self.logger.error("Scooter battery is too low for renting")

class Employee(UserInterface):
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log

    def take_scooter(self, scooter, status_checker):
        rental_type = self.rental_system.determine_rental_type(user_is_employee=True)
        if self._take_scooter(scooter, status_checker, rental_type, "Scooter serviced by employee"):
            scooter.charge_battery()
