"""
================================================================================
Day 20: Python Object-Oriented Programming - Encapsulation Fundamentals
================================================================================
Encapsulation is one of the four foundational pillars of Object-Oriented
Programming (along with Abstraction, Inheritance, and Polymorphism).

Core Definition:
Encapsulation is the bundling of data (attributes) and the methods (functions)
that operate on that data into a single unit (class), while simultaneously
restricting direct outside access to internal implementation details to protect
object integrity.

Core Concepts Covered in this Script:
1. What is Encapsulation & Why does it matter?
2. Public Members (Unrestricted Access)
3. Protected Members (_single_underscore convention)
4. Private Members (__double_underscore mechanism)
5. Comparison: Access from Class, Subclass, and Outside Caller
6. Practical Summary & Architectural Mental Model
================================================================================
"""

def print_separator(title: str):
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


# ==============================================================================
# 1. WHAT IS ENCAPSULATION & THE PROBLEM IT SOLVES
# ==============================================================================
# Without encapsulation, an object's internal state can be directly mutated by
# any external code, causing invalid states, corrupted logic, and tight coupling.

print_separator("1. The Need for Encapsulation (Uncontrolled vs Controlled State)")

# Bad Example: Uncontrolled state (No encapsulation)
class NaiveBankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance  # Completely public and vulnerable to corruption

naive_acc = NaiveBankAccount("Alice", 1000.0)
print(f"[Naive Account] Initial Balance: ${naive_acc.balance:.2f}")

# Anyone from outside can inadvertently or maliciously set invalid data:
naive_acc.balance = -99999.0  # Disastrous! Negative bank balance without rules
print(f"[Naive Account] Corrupted Balance: ${naive_acc.balance:.2f} (Direct Mutation)")


# ==============================================================================
# 2. PUBLIC MEMBERS (Unrestricted Access)
# ==============================================================================
# By default, all attributes and methods in Python classes are PUBLIC.
# Public members can be accessed and modified from anywhere: inside the class,
# inside subclasses, and outside by client code.

print_separator("2. Public Members in Python")

class Smartphone:
    def __init__(self, brand: str, model: str):
        # Public attributes
        self.brand = brand
        self.model = model

    # Public method
    def power_on(self):
        return f"{self.brand} {self.model} is now booting up..."

phone = Smartphone("Google", "Pixel 9 Pro")
# Direct read access
print(f"Phone Brand: {phone.brand}")
print(f"Phone Model: {phone.model}")

# Direct write access
phone.model = "Pixel 9 Pro XL"
print(f"Updated Model: {phone.model}")
print(f"Action Call: {phone.power_on()}")


# ==============================================================================
# 3. PROTECTED MEMBERS (Single Leading Underscore: _attribute)
# ==============================================================================
# In Python, prefixing an attribute or method with a SINGLE underscore `_`
# is a PEP 8 convention indicating that the member is PROTECTED.
#
# IMPORTANT PYTHON TRUTH:
# Python does NOT strictly enforce access control at the compiler level.
# The single underscore is a strong gentleman's agreement among developers:
# "Treat this as internal / non-public API. Do not touch from outside unless
#  you are writing a subclass or you really know what you are doing."

print_separator("3. Protected Members (_single_underscore Convention)")

class Vehicle:
    def __init__(self, make: str, chassis_number: str):
        self.make = make                   # Public
        self._chassis_number = chassis_number  # Protected (internal use)
        self._maintenance_counter = 0      # Protected state

    def _log_diagnostic(self, message: str):
        """Protected helper method intended for internal & derived class usage."""
        self._maintenance_counter += 1
        print(f"[DIAGNOSTIC #{self._maintenance_counter}]: {message} (Chassis: {self._chassis_number})")

    def service_vehicle(self):
        """Public method coordinating internal protected behaviors."""
        print(f"Servicing {self.make}...")
        self._log_diagnostic("Routine 10,000 km inspection completed.")

class ElectricCar(Vehicle):
    """Subclass accessing protected members of the parent."""
    def __init__(self, make: str, chassis_number: str, battery_capacity_kwh: int):
        super().__init__(make, chassis_number)
        self.battery_capacity_kwh = battery_capacity_kwh

    def inspect_battery(self):
        # Subclasses can legitimately access protected parent attributes
        self._log_diagnostic(f"Battery pack checked. Capacity: {self.battery_capacity_kwh} kWh.")

ev = ElectricCar("Tesla", "5YJSA1E28HF123456", 100)
ev.service_vehicle()
ev.inspect_battery()

# Note: Python permits outside access, but code linters and IDEs will warn against it:
print(f"Notice: Protected member accessible, but discouraged by convention: {ev._chassis_number}")


# ==============================================================================
# 4. PRIVATE MEMBERS (Double Leading Underscore: __attribute)
# ==============================================================================
# Prefixing an attribute or method with TWO leading underscores `__` (and at most
# one trailing underscore) triggers Python's NAME MANGLING mechanism.
#
# The interpreter rewrites the attribute name internally as:
# `_ClassName__attributeName`
#
# This makes it impossible to access using the plain attribute name from outside
# or from child classes, preventing accidental override or outside modification.

print_separator("4. Private Members (__double_underscore Mechanism)")

class BankAccount:
    def __init__(self, account_holder: str, initial_balance: float):
        self.account_holder = account_holder     # Public
        self._account_type = "Standard Savings"  # Protected
        self.__balance = initial_balance         # Private (hidden via name mangling)

    # Public method providing controlled read access (Getter)
    def get_balance(self) -> float:
        return self.__balance

    # Public method providing controlled write access (Setter with Validation)
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be strictly positive!")
        self.__balance += amount
        print(f"[+] Successfully deposited ${amount:.2f}. New Balance: ${self.__balance:.2f}")

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly positive!")
        if amount > self.__balance:
            print(f"[-] Transaction declined: Insufficient funds. Balance is only ${self.__balance:.2f}")
            return False
        self.__balance -= amount
        print(f"[+] Successfully withdrew ${amount:.2f}. Remaining Balance: ${self.__balance:.2f}")
        return True

    # Private helper method
    def __calculate_annual_interest(self, rate: float = 0.05) -> float:
        """Internal calculation inaccessible directly from outside."""
        return self.__balance * rate

    def apply_annual_interest(self):
        """Public interface that safely utilizes the private helper."""
        interest = self.__calculate_annual_interest()
        self.__balance += interest
        print(f"[+] Applied annual interest of ${interest:.2f}. New Balance: ${self.__balance:.2f}")

# Instantiation and controlled operations
acc = BankAccount("Sarah Connor", 5000.0)
print(f"Account Holder: {acc.account_holder} (Public)")
print(f"Account Type  : {acc._account_type} (Protected)")
print(f"Account Balance: ${acc.get_balance():.2f} (Retrieved via safe public method)")

# Attempting direct access to private attribute
print("\n[Testing direct access to private attribute '__balance']:")
try:
    print(acc.__balance)
except AttributeError as err:
    print(f" Caught expected AttributeError: {err}")

# Attempting direct access to private method
print("\n[Testing direct call to private method '__calculate_annual_interest']:")
try:
    acc.__calculate_annual_interest()
except AttributeError as err:
    print(f" Caught expected AttributeError: {err}")

# Controlled state mutation through validated methods
print("\n[Executing safe, encapsulated business operations]:")
acc.deposit(1500.0)
acc.withdraw(2000.0)
acc.withdraw(10000.0)  # Attempting overdraft
acc.apply_annual_interest()


# ==============================================================================
# 5. ACCESS SCOPE SUMMARY TABLE
# ==============================================================================
print_separator("5. Access Scope Comparison Summary")

summary = """
+------------------+-----------------------+---------------------+-----------------------+
| Access Level     | Naming Syntax         | Accessible Inside?  | Accessible in Sub?    | Accessible Outside?   |
+------------------+-----------------------+---------------------+-----------------------+
| Public           | self.name             | YES                 | YES                   | YES                   |
| Protected        | self._name            | YES                 | YES (intended)        | YES (discouraged)     |
| Private          | self.__name           | YES                 | NO (name mangled)     | NO (name mangled)     |
+------------------+-----------------------+---------------------+-----------------------+
"""
print(summary)
print("Conclusion: Encapsulation shields internal invariants, simplifies consumer APIs,")
print("and protects objects against unauthorized, corrupting modifications.\n")
