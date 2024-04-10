from abc import ABC, abstractmethod

from logging_setup import log


battery_crytical = 80


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


# Single Responsibility Principle
class Scooter:
    def __init__(self, status, battery_level=100):
        self.status = status
        self.battery_level = battery_level
        self.logger = log

    def change_status(self, new_status):
        if new_status not in ScooterStatus.__dict__.values():
            raise InvalidScooterStatusError(f"Invalid status: {new_status}")
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")

    def is_available(self, user_is_employee: bool):
        if user_is_employee and self.status != ScooterStatus.RENTED:
            return self.status == ScooterStatus.AVAILABLE
        elif not user_is_employee:
            return self.status == ScooterStatus.AVAILABLE and self.battery_level >= battery_crytical

    def battery(self):
        return self.battery_level

    def charge_battery(self):
        self.battery_level = 100
        self.logger.info("Battery fully charged")

    def decrease_battery(self, percentage):
        self.battery_level -= percentage
        if self.battery_level < 0:
            self.battery_level = 0
        if self.battery_level <= battery_crytical:
            self.logger.info(f"! Battery level = {self.battery_level}%")
            self.change_status(ScooterStatus.LOW_BATTERY)

        self.logger.info(f"Battery level decreased by {percentage}% to {self.battery_level}%")


# Dependency Inversion Principle
class CurrentStatus(ABC):
    @abstractmethod
    def check_status(self, scooter):
        pass


class ScooterStatusChecker(CurrentStatus):
    def check_status(self, scooter):
        current_status = scooter.status

        return current_status
