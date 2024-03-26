import unittest
from unittest.mock import patch
from datetime import datetime
from scooter import (
    Scooter,
    ScooterStatus,
    ScooterStatusChecker,
    RentType,
    RentalManager,
    Client,
    Employee,
    RegularRental,
    DiscountedRental,
    ServiceRental,
)


class TestScooter(unittest.TestCase):
    def setUp(self):
        self.scooter = Scooter(ScooterStatus.AVAILABLE)

    def test_change_status(self):
        self.scooter.change_status(ScooterStatus.RENTED)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)

    def test_is_available(self):
        self.assertTrue(self.scooter.is_available())


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.scooter = Scooter(ScooterStatus.AVAILABLE)
        self.status_checker = ScooterStatusChecker()

    def test_rent_scooter(self):
        self.client.rent_scooter(self.scooter, self.status_checker)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = Employee()
        self.scooter = Scooter(ScooterStatus.RENTED)
        self.status_checker = ScooterStatusChecker()

    def test_service_scooter(self):
        self.employee.service_scooter(self.scooter, self.status_checker)
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
        self.rental_manager = RentalManager()
