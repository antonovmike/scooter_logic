from abc import ABC, abstractmethod

from logging_setup import log


class InvalidScooterStatusError(Exception):
    """Raised when an invalid scooter status is attempted to be set."""

    pass


# Single Responsibility Principle
class Scooter:
    def __init__(self, status, battery_level=100):
        self.status = status
        self.battery_level = battery_level # Initialize battery level
        self.logger = log

    def change_status(self, new_status):
        if new_status not in ScooterStatus.__dict__.values():
            raise InvalidScooterStatusError(f"Invalid status: {new_status}")
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")

    def is_available(self):
        return self.status == ScooterStatus.AVAILABLE and self.battery_level >= 20
    
    def battery(self):
        return self.battery_level

    def charge_battery(self):
        self.battery_level = 100
        self.logger.info("Battery fully charged")

    def decrease_battery(self, percentage):
        self.battery_level -= percentage
        if self.battery_level < 0:
            self.battery_level = 0
        self.logger.info(f"Battery level decreased by {percentage}% to {self.battery_level}%")


class ScooterStatus:
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    LOW_BATTERY = "low battery"
    MALFUNCTION = "malfunction"
    SERVICE = "service"
    LOST = "lost"


# Dependency Inversion Principle
class CurrentStatus(ABC):
    @abstractmethod
    def check_status(self, scooter):
        pass


class ScooterStatusChecker(CurrentStatus):
    def check_status(self, scooter):
        current_status = scooter.status
        scooter.logger.info(f"Scooter status is {current_status}")
        return current_status
