from datetime import datetime

from scooter.scooter import ScooterStatus


class RentType:
    REGULAR = "regular"
    DISCOUNTED = "discounted"
    SERVICED = "serviced"


class RentalSystem:
    """
    Manages the rental process for scooters.

    This class is responsible for determining the type of rental based on the user's 
    status and the current time, and for creating the appropriate rental instance.

    Attributes:
    - scooter (Scooter): The scooter being rented.

    Methods:
    - determine_rental_type(user_is_employee: bool) -> str: Determines the rental type 
    based on the user's status and the current time.
    - create_rental_instance(rental_type: str, scooter: Scooter) -> RentalSystem: Creates 
    a rental instance based on the rental type.
    """
    def __init__(self, scooter):
        self.scooter = scooter

    def determine_rental_type(self, user_is_employee):
        """
        Determines the rental type based on the user's status and the current time.

        Parameters:
        - user_is_employee (bool): True if the user is an employee, False otherwise.

        Returns:
        - str: The rental type (REGULAR, DISCOUNTED, or SERVICED).
        """
        current_hour = datetime.now().hour
        if user_is_employee:
            return RentType.SERVICED
        elif 6 <= current_hour < 18:
            return RentType.REGULAR
        else:
            return RentType.DISCOUNTED

    def create_rental_instance(self, rental_type, scooter):
        """
        Creates a rental instance based on the rental type.

        Parameters:
        - rental_type (str): The type of rental (REGULAR, DISCOUNTED, or SERVICED).
        - scooter (Scooter): The scooter being rented.

        Returns:
        - RentalSystem: A rental instance of the appropriate type.

        Raises:
        - ValueError: If the rental type is invalid.
        """
        if rental_type == RentType.SERVICED:
            return ServiceRental(scooter)
        elif rental_type == RentType.REGULAR:
            return RegularRental(scooter)
        elif rental_type == RentType.DISCOUNTED:
            return DiscountedRental(scooter)
        else:
            raise ValueError("Invalid rental type")


class RegularRental(RentalSystem):
    """
    Represents a regular rental of a scooter.

    This class inherits from `RentalSystem` and changes the scooter's status to RENTED upon renting.

    Methods:
    - rent() -> None: Changes the scooter's status to RENTED.
    """
    def rent(self):
        self.scooter.change_status(ScooterStatus.RENTED)


class DiscountedRental(RentalSystem):
    """
    Represents a discounted rental of a scooter.

    This class inherits from `RentalSystem` and changes the scooter's status to RENTED upon renting.

    Methods:
    - rent() -> None: Changes the scooter's status to RENTED.
    """
    def rent(self):
        self.scooter.change_status(ScooterStatus.RENTED)


class ServiceRental(RentalSystem):
    """
    Represents a serviced rental of a scooter.

    This class inherits from `RentalSystem` and changes the scooter's status to SERVICE upon renting.

    Methods:
    - rent() -> None: Changes the scooter's status to SERVICE.
    """
    def rent(self):
        self.scooter.change_status(ScooterStatus.SERVICE)
