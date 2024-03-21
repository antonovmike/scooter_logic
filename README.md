# scooter_logic
Implementing imagined scooters availability system according to SOLID

A simple illustration for my short article ![How can applying the SOLID principles make the code better?](https://dev.to/antonov_mike/how-can-applying-the-solid-principles-make-the-code-better-3fam).

Which SOLID principles are being used in each section:

# Scooter Class
Single Responsibility Principle (SRP): 
The Scooter class has a single responsibility, which is to manage the status of a scooter. It encapsulates the logic related to changing the status and logging relevant information. The change_status method handles only one aspect of the scooter’s behavior.
Open-Closed Principle (OCP): The Scooter class is not explicitly open for extension or closed for modification. However, it adheres to the OCP because its behavior can be extended by creating new subclasses (e.g., RegularRental, DiscountedRental, and ServiceRental) without modifying the existing code.

# ClientInterface and EmployeeInterface Abstract Classes:
Interface Segregation Principle (ISP): These abstract classes define specific methods (rent_scooter for clients and service_scooter for employees) that adhere to the ISP. Clients and employees only need to implement the relevant methods, avoiding unnecessary dependencies.

# Client and Employee Classes:
SRP: Both classes have a single responsibility: Client rents a scooter, and Employee services a scooter. Their methods are focused on their respective tasks.
OCP: These classes are open for extension because they can be subclassed to add more behavior (e.g., additional client or employee actions) without modifying the existing code.

# Rental Base Class and Subclasses (RegularRental, DiscountedRental, and ServiceRental):
Liskov Substitution Principle (LSP): The subclasses (RegularRental, DiscountedRental, and ServiceRental) can be substituted for the base class (Rental) without affecting the correctness of the program. They inherit the common behavior from the base class and specialize it as needed.
SRP: Each subclass has a single responsibility related to renting a scooter with a specific type of rental (regular, discounted, or service).

# RentalSystem Class:
SRP: The RentalSystem class is responsible for handling rentals. Its rent method delegates the actual rental behavior to the injected rental object (which can be any of the subclasses). This separation of concerns adheres to the SRP.
