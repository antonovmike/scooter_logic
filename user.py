from abc import ABC, abstractmethod

from rental_system import RentalSystem
from logging_setup import log


class UserInterface(ABC):
    @abstractmethod
    def take_scooter(self, scooter, status_checker):
        """Blocks the ability to rent or service"""
        pass


class Client(UserInterface):
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log

    def take_scooter(self, scooter, status_checker):
        try:
            if status_checker and scooter.is_available():
                if scooter.battery() > 20:
                    rental_type = self.rental_system.determine_rental_type(user_is_employee=False)
                    rental = self.rental_system.create_rental_instance(rental_type, scooter)
                    rental.rent()
                    self.logger.info("Scooter rented by client")
                    # Deduct 15% battery after client use
                    scooter.decrease_battery(15)
                else:
                    self.logger.error("Scooter battery is too low for renting")
            else:
                self.logger.error(f"Scooter is unavailable for rent: {scooter.status}")
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")


class Employee(UserInterface):
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log

    def take_scooter(self, scooter, status_checker):
        try:
            if status_checker:
                rental_type = self.rental_system.determine_rental_type(user_is_employee=True)
                rental = self.rental_system.create_rental_instance(
                    rental_type, scooter
                )
                rental.rent()
                # Recharge battery in Service
                scooter.charge_battery()
                self.logger.info("Scooter serviced by employee")
            else:
                self.logger.error(f"Unawailable for service: {scooter.status}")
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")

