import unittest
from datetime import datetime

from scooter.scooter import (
    Battery,
    Scooter,
    ScooterStatus,
    ScooterStatusChecker,
    InvalidScooterStatusError,
)
from scooter.user import Client, Employee
from scooter.rental_system import DiscountedRental, RegularRental, RentType, RentalSystem, ServiceRental


class TestScooter(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(100)
        self.scooter = Scooter(ScooterStatus.AVAILABLE, self.battery)

    def test_change_status(self):
        self.scooter.change_status(ScooterStatus.RENTED)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)

    def test_is_available(self):
        self.assertTrue(self.scooter.is_available(False))

    def test_invalid_status_raises_exception(self):
        with self.assertRaises(InvalidScooterStatusError):
            self.scooter.change_status("invalid_status")

    def test_low_battery_status(self):
        scooter = Scooter(ScooterStatus.AVAILABLE, Battery(50))
        scooter.change_status(ScooterStatus.LOW_BATTERY)
        self.assertEqual(scooter.status, ScooterStatus.LOW_BATTERY)


class TestBattery(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(100)
        self.scooter = Scooter(ScooterStatus.AVAILABLE, self.battery)

    def test_battery_level(self):
        self.assertEqual(self.scooter.get_battery_level(), 100)
        self.scooter.decrease_battery(20)
        self.assertEqual(self.scooter.get_battery_level(), 80)

    def test_charge_battery(self):
        self.scooter.decrease_battery(20)
        self.scooter.charge_battery()
        self.assertEqual(self.scooter.get_battery_level(), 100)


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.battery = Battery(100)
        self.scooter = Scooter(ScooterStatus.AVAILABLE, self.battery)
        self.status_checker = ScooterStatusChecker()

    def test_rent_scooter(self):
        self.client.take_scooter(self.scooter, self.status_checker)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = Employee()
        self.battery = Battery(100)
        self.scooter = Scooter(ScooterStatus.AVAILABLE, self.battery)
        self.status_checker = ScooterStatusChecker()

    def test_service_scooter(self):
        self.employee.take_scooter(self.scooter, self.status_checker)
        self.assertEqual(self.scooter.status, ScooterStatus.SERVICE, self.battery)


class TestRental(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(100)
        self.scooter = Scooter(ScooterStatus.AVAILABLE, self.battery)

    def test_regular_rental(self):
        rental = RegularRental(self.scooter)
        rental.rent()
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)

    def test_discounted_rental(self):
        rental = DiscountedRental(self.scooter)
        rental.rent()
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)

    def test_service_rental(self):
        rental = ServiceRental(self.scooter)
        rental.rent()
        self.assertEqual(self.scooter.status, ScooterStatus.SERVICE)


class TestRentalManager(unittest.TestCase):
    def setUp(self):
        self.rental_system = RentalSystem(scooter=None)

    def test_determine_rental_type(self):
        current_hour = datetime.now().hour

        if 6 <= current_hour < 18:
            expect_rent_type = RentType.REGULAR
        else:
            expect_rent_type = RentType.DISCOUNTED

        self.assertEqual(
            self.rental_system.determine_rental_type(user_is_employee=False), 
            expect_rent_type
            )
