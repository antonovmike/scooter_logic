from abc import ABC, abstractmethod

from logging_setup import log
from scooter.scooter import (
    Battery,
    Scooter,
    ScooterStatus,
    ScooterStatusChecker
)

from scooter.user import Client, Employee


battery = Battery(100)
scooter = Scooter(ScooterStatus.AVAILABLE, battery)
client = Client()
employee = Employee()
status_checker = ScooterStatusChecker()
