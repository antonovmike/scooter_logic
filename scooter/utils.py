from scooter.scooter import (
    Battery,
    Scooter,
    ScooterStatus,
    ScooterStatusChecker
)

from scooter.user import Client, Employee


scooter = Scooter(ScooterStatus.AVAILABLE, Battery())
client = Client()
employee = Employee()
status_checker = ScooterStatusChecker()