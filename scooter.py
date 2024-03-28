from abc import ABC, abstractmethod
from datetime import datetime

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class InvalidScooterStatusError(Exception):
    """Raised when an invalid scooter status is attempted to be set."""

    pass


# Single Responsibility Principle
class Scooter:
    def __init__(self, status):
        self.status = status
        self.logger = logging.getLogger(__name__)

    def change_status(self, new_status):
        if new_status not in ScooterStatus.__dict__.values():
            raise InvalidScooterStatusError(f"Invalid status: {new_status}")
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")

    def is_available(self):
        return self.status == ScooterStatus.AVAILABLE


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
