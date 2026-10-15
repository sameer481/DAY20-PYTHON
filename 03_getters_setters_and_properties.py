"""
================================================================================
Day 20: Python Object-Oriented Programming - Getters, Setters, and @property
================================================================================
Encapsulation requires controlled access to an object's internal state.
While other languages (Java, C++, C#) mandate explicit getter and setter methods
for every field, Python provides a far more elegant, pythonic mechanism:
the `@property` decorator.

Core Concepts Covered in this Script:
1. Traditional Getters & Setters (Java/C++ Style) and their Drawbacks
2. The Pythonic Way: `@property` (Getter)
3. Adding Setter Validation with `@<attribute>.setter`
4. Attribute Cleanup Control with `@<attribute>.deleter`
5. Read-Only Computed/Derived Properties
6. Refactoring Advantage: Seamless API Evolution without Breaking Callers
================================================================================
"""

def print_separator(title: str):
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


# ==============================================================================
# 1. TRADITIONAL GETTERS AND SETTERS (Java/C++ Style)
# ==============================================================================
# In languages without properties, developers write get_xxx() and set_xxx() pairs.
# While functional, in Python this produces verbose and un-idiomatic code.

print_separator("1. Traditional Getters and Setters")

class TraditionalEmployee:
    def __init__(self, name: str, salary: float):
        self._name = name
        self._salary = salary

    def get_salary(self) -> float:
        """Traditional getter."""
        return self._salary

    def set_salary(self, new_salary: float):
        """Traditional setter with validation."""
        if not isinstance(new_salary, (int, float)):
            raise TypeError("Salary must be a numeric value!")
        if new_salary < 0:
            raise ValueError("Salary cannot be negative!")
        self._salary = float(new_salary)

emp = TraditionalEmployee("Jordan", 75000.0)
print(f"Initial salary: ${emp.get_salary():.2f}")

emp.set_salary(82000.0)
print(f"Updated salary: ${emp.get_salary():.2f}")

# Why is this un-pythonic?
# It forces developers to invoke methods with parentheses for simple data access.


# ==============================================================================
# 2. THE PYTHONIC WAY: THE @property DECORATOR (GETTER)
# ==============================================================================
# The `@property` decorator turns a method into a read-only attribute getter.
# Users access it using clean attribute syntax: `obj.temperature` (no parentheses).

print_separator("2. Basic @property (Getter)")

class Thermometer:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Getter for celsius temperature."""
        return self._celsius

t = Thermometer(24.5)
# Access like an attribute, but executes the method under the hood:
print(f"Current Temperature: {t.celsius} deg C")
print(f"Is celsius callable? Callable: {callable(t.celsius)}")


# ==============================================================================
# 3. ADDING SETTER VALIDATION: @<attribute>.setter
# ==============================================================================
# To allow modification while retaining complete validation control, define a
# companion method with the same name decorated with `@<attribute_name>.setter`.

print_separator("3. Setter with Validation (@celsius.setter)")

class AdvancedThermometer:
    def __init__(self, celsius: float):
        # We assign via self.celsius so it routes through the setter validation immediately!
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        """Getter."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """Setter with strict physical boundary validation."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"Temperature must be numeric, got {type(value).__name__}!")
        if value < -273.15:
            raise ValueError(
                f"Physically impossible! Temperature {value} deg C is below Absolute Zero (-273.15 deg C)."
            )
        self._celsius = float(value)
        print(f"[+] Temperature successfully calibrated to: {self._celsius:.2f} deg C")

    @property
    def fahrenheit(self) -> float:
        """Dynamically calculated read-only property."""
        return (self._celsius * 9 / 5) + 32

sensor = AdvancedThermometer(20.0)
print(f"In Fahrenheit: {sensor.fahrenheit:.2f} deg F")

# Valid update via setter
sensor.celsius = 37.0
print(f"In Fahrenheit: {sensor.fahrenheit:.2f} deg F")

# Testing validation: Invalid type
print("\n[Testing Invalid Type]:")
try:
    sensor.celsius = "Super Hot"
except TypeError as err:
    print(f"[!] Caught TypeError: {err}")

# Testing validation: Below Absolute Zero
print("\n[Testing Below Absolute Zero]:")
try:
    sensor.celsius = -300.0
except ValueError as err:
    print(f"[!] Caught ValueError: {err}")


# ==============================================================================
# 4. CONTROLLING ATTRIBUTE DELETION: @<attribute>.deleter
# ==============================================================================
# You can intercept `del obj.attribute` using the `@<name>.deleter` decorator.
# This is useful for resetting caches, removing resources, or preventing deletion.

print_separator("4. Deleter Interception (@name.deleter)")

class UserProfile:
    def __init__(self, username: str, email: str):
        self._username = username
        self._email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, new_email: str):
        if "@" not in new_email or "." not in new_email:
            raise ValueError(f"Invalid email address format: '{new_email}'")
        self._email = new_email
        print(f"[+] Email updated to: {self._email}")

    @email.deleter
    def email(self):
        print(f"[!] Deleting email for user '{self._username}'... resetting to default.")
        self._email = "unspecified@example.com"

profile = UserProfile("sameer", "sameer@example.com")
print(f"Current Email: {profile.email}")

# Updating email
profile.email = "sameer.dev@domain.org"

# Deleting email triggers deleter logic instead of destroying the object attribute
del profile.email
print(f"Email after deletion: {profile.email}")


# ==============================================================================
# 5. READ-ONLY COMPUTED / DERIVED PROPERTIES
# ==============================================================================
# Properties are ideal for attributes that depend on other state.
# Instead of storing redundant variables (which can go out of sync), compute
# them on-the-fly!

print_separator("5. Read-Only Computed / Derived Properties")

class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        """Computed on-demand: guaranteed to never be out of sync!"""
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        """Computed on-demand."""
        return 2 * (self.width + self.height)

rect = Rectangle(10.0, 5.0)
print(f"Dimensions: {rect.width} x {rect.height}")
print(f"Area     : {rect.area}")
print(f"Perimeter: {rect.perimeter}")

# Mutating dimension automatically reflects in computed properties:
rect.width = 20.0
print(f"\nAfter updating width to 20.0:")
print(f"Updated Area     : {rect.area}")
print(f"Updated Perimeter: {rect.perimeter}")

# Attempting to assign to a read-only property:
print("\nAttempting to assign directly to rect.area:")
try:
    rect.area = 500.0
except AttributeError as err:
    print(f"[!] Caught expected AttributeError: {err}")


# ==============================================================================
# 6. SEAMLESS REFACTORING ADVANTAGE
# ==============================================================================
print_separator("6. Why Properties Make Python Beautiful: API Compatibility")

explanation = """
In Java or C++, if you start with:
    public double price;
and millions of lines of client code call:
    item.price = 50;
If you later need validation, you are FORCED to change it to:
    item.setPrice(50);
This BREAKS backwards compatibility for all client code!

In Python, you can start with a plain public attribute:
    self.price = 50
And later, if you need validation, you convert it into:
    @property
    def price(self): ...
    @price.setter
    def price(self, val): ...

The client code syntax NEVER changes:
    item.price = 50  <-- Still works seamlessly!
"""
print(explanation)
