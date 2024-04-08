from abc import ABC, abstractmethod

from rental import RentalManager
from logging_setup import log


class UserInterface(ABC):
    @abstractmethod
    def take_scooter(self, scooter, status_checker):
        """Blocks the ability to rent or service"""
        pass


class Client(UserInterface):
    def __init__(self):
        self.rental_manager = RentalManager()
        self.logger = log

    def take_scooter(self, scooter, status_checker):
        try:
            if status_checker:
                # The RentalManager to determine rental type and create Rental instance
                rental_type = self.rental_manager.determine_rental_type(user_is_employee=False)
                rental = self.rental_manager.create_rental_instance(
                    rental_type, scooter
                )
                # The Rental instance to rent the scooter
                rental.rent()
                self.logger.info("Scooter rented by client")
            else:
                self.logger.error(f"Scooter is unavailable for rent: {scooter.status}")
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")


class Employee(UserInterface):
    def __init__(self):
        self.rental_manager = RentalManager()
        self.logger = log

    def take_scooter(self, scooter, status_checker):
        try:
            if status_checker:
                # The RentalManager to determine rental type and create Rental instance
                rental_type = self.rental_manager.determine_rental_type(user_is_employee=True)
                rental = self.rental_manager.create_rental_instance(
                    rental_type, scooter
                )
                # The Rental instance to service the scooter
                rental.rent()
                self.logger.info("Scooter serviced by employee")
            else:
                self.logger.error(f"Unawailable for service: {scooter.status}")
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")

    # def take_scooter(self, scooter, status_checker):
    #     if status_checker:
    #         scooter.change_status("service")
    #         self.logger.info("Scooter serviced by employee")
    #     else:
    #         self.logger.error(f"Unawailable for service: {scooter.status}")
