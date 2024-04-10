# scooter_logic
Implementing imagined scooters availability system according to SOLID

A simple illustration for my short article "[How can applying the SOLID principles make the code better?](https://dev.to/antonov_mike/how-can-applying-the-solid-principles-make-the-code-better-3fam)".

![SOLID](https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fc84v1ezup6sw856i0xgl.jpeg)

An article about developing this app: "[How to put SOLID principles into practice](https://dev.to/antonov_mike/how-to-put-solid-principles-into-practice-3jn3)"

# Which SOLID principles are being used in each section:

## Scooter Class
- SRP: The Scooter class has a single responsibility, which is to manage the status of a scooter. It encapsulates the logic related to changing the status and logging relevant information. The change_status method handles only one aspect of the scooter’s behavior.
- OCP: The Scooter class is not explicitly open for extension or closed for modification. However, it adheres to the OCP because its behavior can be extended by creating new subclasses (e.g., RegularRental, DiscountedRental, and ServiceRental) without modifying the existing code.

## ClientInterface and EmployeeInterface Abstract Classes:
- ISP: These abstract classes define specific methods (rent_scooter for clients and service_scooter for employees) that adhere to the ISP. Clients and employees only need to implement the relevant methods, avoiding unnecessary dependencies.

## Client and Employee Classes:
- SRP: Both classes have a single responsibility: Client rents a scooter, and Employee services a scooter. Their methods are focused on their respective tasks.
- OCP: These classes are open for extension because they can be subclassed to add more behavior (e.g., additional client or employee actions) without modifying the existing code.

## Rental Base Class and Subclasses:
- LSP: The subclasses (RegularRental, DiscountedRental, and ServiceRental) can be substituted for the base class (Rental) without affecting the correctness of the program. They inherit the common behavior from the base class and specialize it as needed.
- SRP: Each subclass has a single responsibility related to renting a scooter with a specific type of rental (regular, discounted, or service).

## RentalSystem Class:
- SRP: The RentalSystem class is responsible for handling rentals. Its rent method delegates the actual rental behavior to the injected rental object (which can be any of the subclasses). This separation of concerns adheres to the SRP.

## CurrentStatus Class:
- DIP: CurrentStatus is an abstraction that defines a check_status method that must be implemented in concrete classes. ScooterStatusChecker implements the CurrentStatus interface by providing a concrete implementation of the check_status method that checks the status of the scooter and logs it. Thus, you can easily replace ScooterStatusChecker with any other CurrentStatus implementation without changing the code that uses CurrentStatus. This follows the principle of abstraction dependency, allowing your code to be more flexible and easily extensible.

## RentalManager Class:
- SRP: It has just one responsibility: managing the rental process. It determines the type of rental based on the time of day and creates the appropriate Rental instance. 
- OCP: To add a new type of rental, we can extend the Rental class and update the create_rental_instance method in RentalManager to handle the new rental type. 

# Dividing into modules

## scooter.py:
Contains the Scooter, ScooterStatus, InvalidScooterStatusError, and ScooterStatusChecker classes. This module will be responsible for managing and checking scooter statuses.

## user.py:
Contains the Client, Employee, and UserInterface classes. This module will be responsible for client and employee interaction with the rental system.

## rental_system.py: 
Contains the RentalSystem class that will be used to manage the rental process. Includes the Rental, RegularRental, DiscountedRental, ServiceRental, and RentalManager classes. This module will handle the scooter rental logic, including defining the rental type and creating rental instances.

## utils.py: 
Can contain common utils such as logging configuration if used in multiple locations.
