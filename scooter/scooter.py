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


class Battery:
    def __init__(self, level=100):
        self.level = level

    def charge(self):
        self.level = 100
        print("Battery fully charged")

    def decrease(self, percentage):
        self.level -= percentage
        if self.level < 0:
            self.level = 0
        if self.level <= battery_crytical:
            print(f"! Battery level = {self.level}%")

    def get_level(self):
        return self.level


class Scooter:
    def __init__(self, status, battery: Battery):
        self.status = status
        self.battery = battery
        self.logger = log

    def change_status(self, new_status):
        if new_status not in ScooterStatus.__dict__.values():
            raise InvalidScooterStatusError(f"Invalid status: {new_status}")
        self.status = new_status
        self.logger.info(f"Scooter status changed to {new_status}")
        if self.battery.get_level() <= battery_crytical:
            self.status = ScooterStatus.LOW_BATTERY
            return self.status
        if new_status == ScooterStatus.AVAILABLE:
            return self.status
        else:
            return self.status

    def is_available(self, user_is_employee: bool):
        if self.get_battery_level() <= battery_crytical:
            return self.status == ScooterStatus.LOW_BATTERY
        elif user_is_employee and self.status != ScooterStatus.RENTED:
            return self.status == ScooterStatus.AVAILABLE
        elif not user_is_employee:
            return self.status == ScooterStatus.AVAILABLE and self.get_battery_level() >= battery_crytical

    def get_battery_level(self):
        return self.battery.get_level()

    def charge_battery(self):
        self.battery.charge()

        return self.battery.get_level()

    def decrease_battery(self, percentage):
        self.battery.decrease(percentage)

        return self.battery.get_level()


# Dependency Inversion Principle
class CurrentStatus(ABC):
    @abstractmethod
    def check_status(self, scooter):
        pass


class ScooterStatusChecker(CurrentStatus):
    def check_status(self, scooter):
        current_status = scooter.status

        return current_status
