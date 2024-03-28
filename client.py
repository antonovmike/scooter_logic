from abc import ABC, abstractmethod

from scooter import RentalManager

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class ClientInterface(ABC):
    @abstractmethod
    def rent_scooter(self, scooter, status_checker):
        """Rent a scooter."""
        pass


class EmployeeInterface(ABC):
    @abstractmethod
    def service_scooter(self, scooter, status_checker):
        """Service a scooter."""
        pass


class Client(ClientInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rental_manager = RentalManager()

    def rent_scooter(self, scooter, status_checker):
        try:
            if status_checker:
                # Use RentalManager to determine the rental type and create the Rental instance
                rental_type = self.rental_manager.determine_rental_type()
                rental = self.rental_manager.create_rental_instance(
                    rental_type, scooter
                )
                # Use the Rental instance to rent the scooter
                rental.rent()
                self.logger.info("Scooter rented by client")
            else:
                self.logger.error(f"Scooter is unavailable for rent: {scooter.status}")
        except Exception as e:
            self.logger.error(f"An error occurred while renting the scooter: {e}")


class Employee(EmployeeInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def service_scooter(self, scooter, status_checker):
        if status_checker:
            scooter.change_status("service")
            self.logger.info("Scooter serviced by employee")
        else:
            self.logger.error(f"Unawailable for service: {scooter.status}")
