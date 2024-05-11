from abc import ABC, abstractmethod

from scooter.rental_system import RentType, RentalSystem
from scooter.scooter import Battery, Scooter, ScooterStatusChecker
from logging_setup import log


class UserInterface(ABC):
    @abstractmethod
    def take_scooter(self, scooter: Scooter, status_checker: bool):
        """Blocks the ability to rent or service"""
        pass

    def _take_scooter(
            self, scooter: Scooter, status_checker: ScooterStatusChecker, rental_type: RentType, 
            action_description: str, user_is_employee: bool
            ):
        """
        Takes the scooter based on the provided status checker and rental type.

        Parameters:
        - scooter (Scooter): The scooter to take.
        - status_checker (ScooterStatusChecker): The status checker to use.
        - rental_type (RentType): The type of rental to use.
        - action_description (str): The description of the action being taken.
        """
        try:
            if status_checker:
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
    """Represents a client in the system."""
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log
        self.user_is_employee = False
        self.is_employee_repairer = False

    def take_scooter(self, scooter: Scooter, status_checker: ScooterStatusChecker) -> bool:
        """
        Takes the scooter based on the provided status checker.

        Parameters:
        - scooter (Scooter): The scooter to take.
        - status_checker (ScooterStatusChecker): The status checker to use.

        Returns:
        - bool: True if the scooter was taken successfully, False otherwise.
        """
        if scooter.get_battery_level() >= Battery.battery_low(scooter.get_battery_level()):
            rental_type = self.rental_system.determine_rental_type(self.user_is_employee)
            if self._take_scooter(
                    scooter, status_checker, rental_type, 
                    "Scooter rented by client", self.user_is_employee
                    ):
                scooter.decrease_battery(15)
                return scooter.status
            return scooter.status
        else:
            self.logger.error("Scooter battery is too low for renting")
            return scooter.status


class Employee(UserInterface):
    """Represents an employee in the system."""
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log
        self.user_is_employee = True
        self.is_employee_repairer = False

    def take_scooter(self, scooter: Scooter, status_checker: ScooterStatusChecker) -> bool:
        """
        Takes the scooter based on the provided status checker.
        
        Parameters:
        - scooter (Scooter): The scooter to take.
        - status_checker (ScooterStatusChecker): The status checker to use.

        Returns:
        - bool: True if the scooter was taken successfully, False otherwise.
        """
        rental_type = self.rental_system.determine_rental_type(self.user_is_employee)
        if self._take_scooter(
                scooter, status_checker, rental_type, 
                "Scooter serviced by employee", self.user_is_employee
                ):
            scooter.charge_battery()
            return scooter.status
        else:
            return scooter.status


class Repairer(UserInterface):
    """Represents a repairer in the system."""
    def __init__(self):
        self.rental_system = RentalSystem(scooter=None)
        self.logger = log
        self.user_is_employee = True
        self.is_employee_repairer = True

    def take_scooter(self, scooter: Scooter, status_checker: ScooterStatusChecker) -> bool:
        rental_type = self.rental_system.determine_rental_type(self.user_is_employee)
        if self._take_scooter(
                scooter, status_checker, rental_type, 
                "Scooter repaired by repairer", self.user_is_employee
                ):
            scooter.charge_battery()
            return scooter.status
        else:
            return scooter.status
