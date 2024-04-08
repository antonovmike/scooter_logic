import unittest
from datetime import datetime

from scooter import (
    Scooter,
    ScooterStatus,
    ScooterStatusChecker,
    InvalidScooterStatusError,
)
from user import Client, Employee
from rental_system import DiscountedRental, RegularRental, RentType, RentalSystem, ServiceRental


class TestScooter(unittest.TestCase):
    def setUp(self):
        self.scooter = Scooter(ScooterStatus.AVAILABLE)

    def test_change_status(self):
        self.scooter.change_status(ScooterStatus.RENTED)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)

    def test_is_available(self):
        self.assertTrue(self.scooter.is_available())

    def test_invalid_status_raises_exception(self):
        with self.assertRaises(InvalidScooterStatusError):
            self.scooter.change_status("invalid_status")


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.scooter = Scooter(ScooterStatus.AVAILABLE)
        self.status_checker = ScooterStatusChecker()

    def test_rent_scooter(self):
        self.client.take_scooter(self.scooter, self.status_checker)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = Employee()
        self.scooter = Scooter(ScooterStatus.SERVICE)
        self.status_checker = ScooterStatusChecker()

    def test_service_scooter(self):
        self.employee.take_scooter(self.scooter, self.status_checker)
        self.assertEqual(self.scooter.status, ScooterStatus.SERVICE)


class TestRental(unittest.TestCase):
    def setUp(self):
        self.scooter = Scooter(ScooterStatus.AVAILABLE)

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

        self.assertEqual(self.rental_system.determine_rental_type(user_is_employee=False), expect_rent_type)
