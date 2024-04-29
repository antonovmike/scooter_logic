from abc import ABC, abstractmethod

from logging_setup import log


class InvalidScooterStatusError(Exception):
    """Raised when an invalid scooter status is attempted to be set."""

    pass


class ScooterStatus:
    AVAILABLE = "available"
    LOST = "lost"
    LOW_BATTERY = "low battery"
    MALFUNCTION = "malfunction"
    RESERVED = "reserved"
    RENTED = "rented"
    SERVICE = "service"


class Battery:
    """Represents a scooter battery."""
    def __init__(self, level=100, battery_crytical=20):
        self.level = level
        self.battery_crytical = battery_crytical

    def charge(self):
        """Charges the battery to 100%."""
        self.level = 100
        print("Battery fully charged")

    def decrease(self, percentage):
        """
        Decreases the battery level by the specified percentage.

        Parameters:
        - percentage (int): The percentage to decrease the battery level by.
        """
        self.level -= percentage
        if self.level < 0:
            self.level = 0
        if self.level <= self.battery_crytical:
            print(f"! Battery level = {self.level}%")

    def get_level(self):
        """
        Returns the current battery level.

        Returns:
        - int: The current battery level.
        """
        return self.level


class Scooter:
    """Represents a scooter."""
    def __init__(self, status, battery: Battery):
        self.status = status
        self.battery = battery
        self.logger = log

    def change_status(self, new_status):
        """
        Changes the status of the scooter.

        Parameters:
        - new_status (str): The new status of the scooter.

        Raises:
        - InvalidScooterStatusError: If the new status is not valid.
        """
        if new_status not in ScooterStatus.__dict__.values():
            raise InvalidScooterStatusError(f"Invalid status: {new_status}")
        
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")

        if self.battery.get_level() <= self.battery.battery_crytical:
            self.status = ScooterStatus.LOW_BATTERY

        return self.status

    def is_available(self, user_is_employee: bool):
        """
        Checks if the scooter is available for use.

        Parameters:
        - user_is_employee (bool): Indicates whether the user is an employee.

        Returns:
        - bool: True if the scooter is available, False otherwise.
        """
        if self.get_battery_level() <= self.battery.battery_crytical:
            return self.status == ScooterStatus.LOW_BATTERY
        elif user_is_employee and self.status != ScooterStatus.RENTED:
            return self.status == ScooterStatus.AVAILABLE
        elif not user_is_employee:
            return self.status == ScooterStatus.AVAILABLE and self.get_battery_level() >= self.battery.battery_crytical

    def get_battery_level(self):
        """Returns the current battery level."""
        return self.battery.get_level()

    def charge_battery(self):
        """Charges the scooter battery."""
        self.battery.charge()

    def decrease_battery(self, percentage):
        """
        Decreases the scooter battery by the specified percentage.

        Parameters:
        - percentage (int): The percentage to decrease the battery by.
        """
        self.battery.decrease(percentage)


# Dependency Inversion Principle
class CurrentStatus(ABC):
    """Abstract class representing the current status of a scooter."""
    @abstractmethod
    def check_status(self, scooter):
        pass


class ScooterStatusChecker(CurrentStatus):
    """Checks the current status of the scooter."""
    def check_status(self, scooter):
        """
        Checks the current status of the scooter.

        Parameters:
        - scooter (Scooter): The scooter to check the status of.

        Returns:
        - str: The current status of the scooter.
        """
        current_status = scooter.status

        return current_status
