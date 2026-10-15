"""
================================================================================
Day 20: Python Object-Oriented Programming - Advanced Encapsulation & Safety
================================================================================
Encapsulation goes far beyond prefixing variable names with underscores.
In professional production systems, proper encapsulation involves:
- Protecting mutable structures from external leaks (Defensive Copying)
- Restricting dynamic attribute monkey-patching (`__slots__`)
- Distinguishing clearly between Encapsulation and Abstraction
- Designing clean, cohesive public APIs while hiding internal orchestration

Core Concepts Covered in this Script:
1. Encapsulation vs. Abstraction: The Vital Distinction
2. Defensive Copying: Preventing Mutable State Leaks
3. Restricting Dynamic Attributes using `__slots__`
4. Encapsulated Workflow Orchestration (Facade / Internal Helpers)
5. Production Best Practices & Architectural Checklist
================================================================================
"""

def print_separator(title: str):
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


# ==============================================================================
# 1. ENCAPSULATION VS ABSTRACTION: THE VITAL DISTINCTION
# ==============================================================================
# Many developers confuse Encapsulation with Abstraction.
# - Encapsulation is INFORMATION HIDING & BUNDLING:
#     "Hide the data and implementation details inside the capsule."
# - Abstraction is COMPLEXITY REDUCTION:
#     "Show ONLY what the user needs to know to operate the system."

print_separator("1. Encapsulation vs. Abstraction")

comparison = """
+------------------------+-------------------------------------------------------+
| Feature                | Description                                           |
+------------------------+-------------------------------------------------------+
| Focus of Encapsulation | "How is data protected and bundled with behavior?"    |
| Focus of Abstraction   | "What does the object do, rather than how it does it?"|
| Mechanism              | Access modifiers, @property, defensive copies.        |
| Real-World Analogy     | Medicine Capsule: the bitter medicine compounds are   |
|                        | safely sealed inside a gelatin capsule shell.         |
| Abstraction Analogy    | Car Steering Wheel & Accelerator pedal: you drive the |
|                        | vehicle without knowing fuel injection telemetry.     |
+------------------------+-------------------------------------------------------+
"""
print(comparison)


# ==============================================================================
# 2. DEFENSIVE COPYING: PREVENTING MUTABLE STATE LEAKS
# ==============================================================================
# A common pitfall in Python encapsulation:
# If an attribute is a mutable object (like a list, dictionary, or set),
# simply marking it private (`self.__items`) or using `@property` IS NOT ENOUGH
# if your getter returns the direct reference to the mutable container!
#
# Client code can mutate the container in-place and bypass all class invariants!

print_separator("2. Defensive Copying: Preventing Mutable State Leaks")

# VULNERABLE CLASS: Leaks internal mutable list
class LeakyCart:
    def __init__(self):
        self.__items = []

    def add_item(self, item: str):
        if not isinstance(item, str) or len(item.strip()) == 0:
            raise ValueError("Item must be a non-empty string!")
        self.__items.append(item.strip())

    @property
    def items(self) -> list:
        # BUG: Returning the internal mutable list directly!
        return self.__items

# SECURE CLASS: Employs defensive copying
class SecureCart:
    def __init__(self):
        self.__items = []

    def add_item(self, item: str):
        if not isinstance(item, str) or len(item.strip()) == 0:
            raise ValueError("Item must be a non-empty string!")
        self.__items.append(item.strip())

    @property
    def items(self) -> tuple:
        # FIX: Return an immutable tuple or a shallow copy (.copy())
        # Returning a tuple ensures external callers CANNOT append or delete in-place!
        return tuple(self.__items)

print("[Testing LeakyCart Vulnerability]:")
leaky = LeakyCart()
leaky.add_item("Mechanical Keyboard")
print(f"Cart before: {leaky.items}")

# External code mutates internal list directly through the returned reference:
leaky.items.append("!!! Corrupted Injected Item Without Validation !!!")
print(f"Cart after direct leak mutation: {leaky.items} (State Corrupted!)")

print("\n[Testing SecureCart Defensive Copying]:")
secure = SecureCart()
secure.add_item("Studio Headphones")
print(f"Secure Cart before: {secure.items}")

try:
    # Attempting to mutate the returned tuple directly:
    secure.items.append("Malicious Injection")
except AttributeError as err:
    print(f"[+] Protection Successful! Blocked modification: {err}")


# ==============================================================================
# 3. RESTRICTING DYNAMIC ATTRIBUTES WITH __slots__
# ==============================================================================
# By default, Python objects allow assigning arbitrary attributes at any time:
#   obj.any_random_name = 42
# This can lead to bugs caused by typos (e.g. `acc.balence = 100` instead of `balance`).
#
# Using `__slots__`:
# 1. Restricts attributes strictly to a predefined whitelist.
# 2. Eliminates `__dict__`, reducing memory footprint significantly (up to 40-50%).
# 3. Enforces strict attribute encapsulation against accidental additions.

print_separator("3. Enforcing Attribute Bounds with __slots__")

class StrictCoordinate:
    # Whitelist of allowed attributes for every instance of this class
    __slots__ = ("_x", "_y")

    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val: float):
        self._x = float(val)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val: float):
        self._y = float(val)

    def __repr__(self) -> str:
        return f"StrictCoordinate(x={self._x}, y={self._y})"

coord = StrictCoordinate(12.5, 84.3)
print(f"Coordinate: {coord}")

# Normal valid setter
coord.x = 15.0
print(f"Updated Coordinate: {coord}")

# Attempting to add an accidental arbitrary attribute:
print("\nAttempting to assign an unauthorized attribute 'coord.z = 99':")
try:
    coord.z = 99.0
except AttributeError as err:
    print(f"[!] Blocked by __slots__: {err}")


# ==============================================================================
# 4. ENCAPSULATED WORKFLOW ORCHESTRATION (INTERNAL HELPERS)
# ==============================================================================
# Encapsulation allows you to present a single, clean public method
# while managing a complex web of internal state transitions and checks.

print_separator("4. Encapsulated Multi-Step Workflow Orchestration")

class CloudDeploymentPipeline:
    def __init__(self, app_name: str, environment: str):
        self.app_name = app_name
        self._environment = environment
        self._state = "IDLE"
        self._logs = []

    @property
    def current_state(self) -> str:
        return self._state

    def deploy(self) -> bool:
        """Single clean public method exposing the entire operation."""
        print(f"\n[PIPELINE] Initiating deployment for '{self.app_name}' to {self._environment}...")
        try:
            self._transition_to("VALIDATING")
            self._validate_configurations()

            self._transition_to("BUILDING")
            self._build_container_image()

            self._transition_to("DEPLOYING")
            self._rollout_to_cluster()

            self._transition_to("HEALTH_CHECK")
            self._verify_health_probes()

            self._transition_to("COMPLETED")
            print(f"[+] Deployment SUCCESS for '{self.app_name}'!")
            return True
        except Exception as err:
            self._transition_to("FAILED")
            print(f"[-] Deployment FAILED: {err}")
            return False

    # Private/Protected internal step helpers:
    def _transition_to(self, new_state: str):
        self._state = new_state
        entry = f"State changed to {new_state}"
        self._logs.append(entry)
        print(f"  -> [STATE]: {new_state}")

    def _validate_configurations(self):
        print("     Checking environment variables and secrets...")

    def _build_container_image(self):
        print("     Compiling assets and building Docker container...")

    def _rollout_to_cluster(self):
        print("     Executing rolling update across Kubernetes worker nodes...")

    def _verify_health_probes(self):
        print("     Probing /healthz endpoints... 200 OK.")

pipeline = CloudDeploymentPipeline("payment-microservice", "production")
pipeline.deploy()
print(f"Final Pipeline State: {pipeline.current_state}")
