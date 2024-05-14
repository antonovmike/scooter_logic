from scooter.scooter import (
    Scooter,
    ScooterStatus,
    ScooterStatusChecker
)

from scooter.user import Client, Employee


scooter = Scooter(ScooterStatus.AVAILABLE)
client = Client()
employee = Employee()
status_checker = ScooterStatusChecker()
