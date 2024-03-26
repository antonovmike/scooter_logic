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
    RegularRental,
    DiscountedRental,
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
        # This test assumes that the scooter is available and the status checker allows renting
        self.client.rent_scooter(self.scooter, self.status_checker)
        self.assertEqual(self.scooter.status, ScooterStatus.RENTED)


# class TestEmployee(unittest.TestCase):
#     pass

# class TestRental(unittest.TestCase):
#     pass

# class TestRentalManager(unittest.TestCase):
#     pass
