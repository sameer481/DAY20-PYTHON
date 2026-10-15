"""
================================================================================
Day 20: Python Object-Oriented Programming - Name Mangling Deep Dive
================================================================================
In Python, "private" attributes are not strictly locked away behind hardware
or compiler walls. Instead, Python uses a clever, deterministic mechanism
called NAME MANGLING.

Core Definition:
Any identifier with at least two leading underscores (e.g., `__attr`) and at
most one trailing underscore is textually replaced by the Python compiler
with `_ClassName__attr`, where `ClassName` is the current class name stripped
of any leading underscores.

Core Concepts Covered in this Script:
1. The Name Mangling Transformation Mechanism
2. Introspecting Object Internals with `__dict__` and `dir()`
3. Accessing Mangled Names (The "Consenting Adults" Philosophy)
4. The Real Purpose of Mangling: Preventing Subclass Collision
5. Mangling of Private Methods
6. Common Anti-Patterns and Best Practices
================================================================================
"""

def print_separator(title: str):
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


# ==============================================================================
# 1. THE NAME MANGLING TRANSFORMATION MECHANISM
# ==============================================================================
# When you write `self.__secret = value` inside a class named `Vault`,
# Python transparently translates that attribute name to `_Vault__secret`.

print_separator("1. How Python Rewrites Private Attribute Names")

class Vault:
    def __init__(self, owner: str, passcode: str):
        self.owner = owner          # Public
        self.__passcode = passcode  # Private -> rewritten as _Vault__passcode

    def reveal_passcode(self) -> str:
        """Internal class code uses the natural __passcode syntax."""
        return f"[Vault Internal] Passcode is: {self.__passcode}"

my_vault = Vault("Alex", "AlphaOmega99#")

print(f"Vault Owner: {my_vault.owner}")
print(f"Method call: {my_vault.reveal_passcode()}")

print("\nAttempting to access my_vault.__passcode directly:")
try:
    print(my_vault.__passcode)
except AttributeError as err:
    print(f"[!] Access Denied as expected: {err}")


# ==============================================================================
# 2. INTROSPECTING OBJECT INTERNALS: __dict__ and dir()
# ==============================================================================
# In Python, an object's instance attributes are stored in a standard dictionary
# called `__dict__`. We can inspect this dictionary directly to observe mangling!

print_separator("2. Introspecting Object Memory via __dict__ and dir()")

print("Inspecting my_vault.__dict__:")
for key, val in my_vault.__dict__.items():
    print(f"  Key in __dict__: '{key}' => Value: '{val}'")

print("\nNotice that '__passcode' DOES NOT exist in the dictionary.")
print("Instead, Python stored it under the mangled key: '_Vault__passcode'!")

# Using dir() to inspect all available attributes on the object:
all_attributes = dir(my_vault)
mangled_found = [attr for attr in all_attributes if "passcode" in attr]
print(f"\nFiltered dir() matching 'passcode': {mangled_found}")


# ==============================================================================
# 3. ACCESSING MANGLED NAMES: "WE ARE ALL CONSENTING ADULTS HERE"
# ==============================================================================
# Python creator Guido van Rossum famously stated:
# "We are all consenting adults here."
#
# Python does not treat developers as untrustworthy adversaries.
# If an engineer explicitly accesses `_Vault__passcode`, Python will NOT stop them,
# but doing so breaks the encapsulation contract and risks regressions.

print_separator("3. Direct Access via Mangled Name (And Why It's Dangerous)")

# Accessing using the mangled name directly:
bypassed_passcode = my_vault._Vault__passcode
print(f"[!] Bypassed via mangled name: {bypassed_passcode}")

# We can even modify it (although strongly discouraged in production):
my_vault._Vault__passcode = "NewSuperSecret456!"
print(f"[!] Force-modified via mangled name: {my_vault.reveal_passcode()}")

print("\nWhy is bypassing name mangling considered an anti-pattern?")
print("1. It tightly couples external code to internal private implementation.")
print("2. If the class name or attribute name changes during a refactor, external code breaks.")
print("3. It circumvents business validations, creating potential data corruption.")


# ==============================================================================
# 4. THE REAL PURPOSE: PREVENTING INHERITANCE ACCIDENTAL COLLISIONS
# ==============================================================================
# The primary design reason Python introduced double underscore name mangling
# is NOT security or cryptography; it is to PREVENT SUBCLASS NAME CLASHES.
#
# Imagine a base class and a derived class that both happen to use an internal
# state variable with the same common name (e.g. `__id`, `__cache`, `__config`).
# Without mangling, the child's attribute would overwrite the parent's attribute!

print_separator("4. Preventing Namespace Collisions in Inheritance Hierarchies")

class BaseService:
    def __init__(self, service_id: str):
        # Mangled to: _BaseService__id
        self.__id = service_id
        # Mangled to: _BaseService__cache
        self.__cache = ["init_base_cache"]

    def base_summary(self):
        return f"[BaseService] ID: {self.__id}, Cache: {self.__cache}"

class CloudService(BaseService):
    def __init__(self, service_id: str, cloud_region: str):
        super().__init__(service_id)
        self.region = cloud_region
        # Subclass also uses a variable named __id and __cache for its own needs!
        # Mangled to: _CloudService__id
        self.__id = f"CLOUD-{service_id.upper()}-{cloud_region}"
        # Mangled to: _CloudService__cache
        self.__cache = {"region": cloud_region, "status": "active"}

    def cloud_summary(self):
        return f"[CloudService] Subclass ID: {self.__id}, Subclass Cache: {self.__cache}"

service = CloudService("svc-9901", "us-east-1")

print("Let's inspect how both classes co-exist in the same instance memory:")
print(service.base_summary())
print(service.cloud_summary())

print("\nInstance dictionary showing separate namespaces:")
for k, v in service.__dict__.items():
    print(f"  {k} -> {v}")

print("\nObservation:")
print("Both `_BaseService__id` and `_CloudService__id` exist safely in memory!")
print("Neither class accidentally overwrote the other's internal state.")


# ==============================================================================
# 5. MANGLING OF PRIVATE METHODS
# ==============================================================================
# Just like attributes, methods starting with `__` are also name-mangled.
# This prevents derived classes from accidentally overriding internal machinery.

print_separator("5. Private Methods Mangling")

class PaymentGateway:
    def process_transaction(self, amount: float):
        print(f"[Public Interface] Initiating charge for ${amount:.2f}")
        self.__sanitize_request()
        self.__execute_secure_rpc(amount)
        print("[Public Interface] Transaction completed successfully.")

    # Private method -> _PaymentGateway__sanitize_request
    def __sanitize_request(self):
        print("  [Private Helper] Sanitizing payload and stripping headers...")

    # Private method -> _PaymentGateway__execute_secure_rpc
    def __execute_secure_rpc(self, amount: float):
        print(f"  [Private Helper] Executing encrypted RPC call for ${amount:.2f}...")

gateway = PaymentGateway()
gateway.process_transaction(249.99)

print("\nAttempting to call gateway.__sanitize_request():")
try:
    gateway.__sanitize_request()
except AttributeError as err:
    print(f"[!] Blocked as expected: {err}")

print(f"[!] Can only be invoked externally via mangled identifier: _PaymentGateway__sanitize_request")


# ==============================================================================
# 6. RULES OF THUMB FOR PYTHON ACCESS CONVENTIONS
# ==============================================================================
print_separator("6. Rules of Thumb: When to use _, __, or Plain Names")

rules = """
+--------------------+-----------------------------+----------------------------------------------+
| Syntax             | Concept                     | Recommended Use Case                         |
+--------------------+-----------------------------+----------------------------------------------+
| name               | Public                      | Standard attributes & public API interface.  |
| _name              | Protected / Internal        | Internal implementation details (PEP 8).     |
|                    |                             | Most common & pythonic way to signal privacy.|
| __name             | Private (Mangled)           | Avoid namespace collision in inheritance.    |
|                    |                             | Deep defensive state protection.             |
| __name__           | Special / Dunder Method     | Reserved for Python core system (dunder).    |
|                    |                             | NEVER create your own custom __dunders__!    |
+--------------------+-----------------------------+----------------------------------------------+
"""
print(rules)
