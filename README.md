# Day 20: Python Object-Oriented Programming (OOP) - Encapsulation 🛡️

Welcome to **Day 20** of the Python Mastery Series! Today's masterclass is dedicated to **Encapsulation**, one of the four core pillars of Object-Oriented Programming (OOP), alongside Abstraction, Inheritance, and Polymorphism.

Encapsulation is the art and discipline of **bundling data (attributes) and behavior (methods)** into a single unit (class), while **restricting unauthorized direct access** to internal implementation details to preserve object integrity and guarantee business rules.

---

## 📁 Repository Structure

```text
DAY20-PYTHON/
│
├── 01_encapsulation_fundamentals.py       # Public, protected (_), and private (__) members
├── 02_name_mangling_deep_dive.py          # Python's name mangling mechanics & namespace collision defense
├── 03_getters_setters_and_properties.py   # Pythonic @property, setters, deleters & calculated fields
├── 04_advanced_encapsulation_and_safety.py# Defensive copying, mutable state leaks, and __slots__
├── 05_practical_projects.py               # 3 Real-world production projects (Banking, Payroll, Auth Vault)
├── .gitignore                             # Python bytecode, virtualenv & system exclusions
└── README.md                              # Comprehensive masterclass guide & conceptual walkthrough
```

---

## 🧭 Why Encapsulation Matters

In uncontrolled procedural or naive OOP code, an object's state is exposed directly to the outside world:

```text
[ External Caller ]  ==== Direct Write ====>  acc.balance = -99999.00  (Corrupted State!)
```

With **Encapsulation**, the object controls its boundary through validated methods and properties:

```text
                               +------------------------------------+
                               |          ENCAPSULATED CLASS        |
                               |                                    |
[ External Caller ]            |  +------------------------------+  |
       |                       |  | Private State:               |  |
       |-- deposit(500) ------>|  |  self.__balance = 1500.0     |  |
       |   (Validated)         |  +------------------------------+  |
       |                       |  | Public Interface:            |  |
       |                       |  |  - deposit(amount)           |  |
       |<-- Returns Balance ---|  |  - withdraw(amount)          |  |
                               |  |  - @property balance         |  |
                               |  +------------------------------+  |
                               +------------------------------------+
```

### Key Benefits:
- **Data Protection & Integrity**: Prevents external code from setting impossible or corrupt values (e.g., negative balances, temperatures below absolute zero).
- **Decoupled Architecture**: You can change internal implementation details (e.g. data structures or calculations) without breaking code that uses your class.
- **Maintainability & Evolution**: Start with simple attributes and upgrade to validated `@property` methods later with zero breaking changes for callers.
- **Clear Public API**: Consumers interact with an intentional, clean interface rather than complex internal machinery.

---

## 📚 Core Concepts & Architectural Walkthrough

### 1. Access Modifiers in Python

Unlike languages such as Java or C++ that enforce access control at the compiler level, Python relies on conventions and deterministic name transformations.

| Access Level | Naming Convention | Accessible Inside Class? | Accessible in Subclass? | Accessible from Outside? | Intended Purpose |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Public** | `self.name` |  YES |  YES |  YES | Standard attributes and public API methods. |
| **Protected** | `self._name` |  YES |  YES | ⚠️ Discouraged | Internal implementation details. "Gentleman's agreement" (PEP 8). |
| **Private** | `self.__name` |  YES | ❌ Mangled | ❌ Mangled | Triggers Name Mangling (`_Class__name`). Prevents collision in subclasses. |

```python
class Smartphone:
    def __init__(self, brand: str, imei: str, pin: str):
        self.brand = brand       # Public
        self._imei = imei        # Protected (internal convention)
        self.__pin = pin         # Private (name mangled)
```

---

### 2. The Mechanics of Name Mangling

When Python compiles an identifier with **two or more leading underscores** and at most one trailing underscore, it rewrites the identifier into:

$$\text{\_ClassName\_\_attributeName}$$

```python
class Vault:
    def __init__(self, secret: str):
        self.__secret = secret

v = Vault("TopSecret123")

# Direct access raises an AttributeError:
# print(v.__secret) -> AttributeError: 'Vault' object has no attribute '__secret'

# Python rewrote the key inside instance.__dict__:
print(v._Vault__secret)  # "TopSecret123"
```

#### Why Name Mangling Exists: Preventing Subclass Collision
The primary design reason for name mangling is **preventing accidental collisions in class inheritance hierarchies**. If a parent class and a derived child class both define `self.__id`, mangling keeps them completely isolated in memory:
- Parent holds: `_BaseService__id`
- Child holds: `_CloudService__id`

Neither overrides or corrupts the other!

---

### 3. Pythonic Encapsulation with `@property`

In traditional languages, developers are forced to write verbose getter and setter methods (`getSalary()`, `setSalary()`). Python provides the `@property` decorator, enabling clean attribute syntax while executing validation logic under the hood.

```python
class Thermometer:
    def __init__(self, celsius: float):
        self.celsius = celsius  # Routes through the setter immediately!

    @property
    def celsius(self) -> float:
        """Getter: Called when reading sensor.celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """Setter: Called when writing sensor.celsius = 30"""
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be numeric!")
        if value < -273.15:
            raise ValueError("Temperature cannot be below Absolute Zero (-273.15 C)!")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        """Read-only computed property: dynamic conversion"""
        return (self._celsius * 9 / 5) + 32
```

#### Benefits of `@property`:
1. **Attribute Syntax**: Call `sensor.celsius` instead of `sensor.get_celsius()`.
2. **Backwards Compatibility**: Start with a plain attribute `self.price = 10`. If you later need validation, convert it to a property **without breaking existing callers**.
3. **Read-Only Derived Values**: Easily expose calculated properties (like `area`, `bmi`, or `fahrenheit`) that never get out of sync.

---

### 4. Defensive Copying: Preventing Mutable State Leaks

A subtle and dangerous vulnerability occurs when an encapsulated class exposes a mutable collection (e.g., `list`, `dict`, `set`) via a getter:

```python
# VULNERABLE:
class LeakyCart:
    def __init__(self):
        self.__items = []

    @property
    def items(self):
        return self.__items  # LEAK! External code can call cart.items.append(...)!

# SECURE (Defensive Copying):
class SecureCart:
    def __init__(self):
        self.__items = []

    @property
    def items(self):
        return tuple(self.__items)  # Safe! Returns an immutable view/copy
```

---

### 5. Memory & Bounds Enforcement with `__slots__`

By default, Python objects store attributes in a dynamic dictionary `__dict__`, which permits dynamic monkey-patching. By specifying `__slots__`, you restrict an object to a fixed set of attributes, drastically reduce memory usage, and prevent accidental typo bugs.

```python
class StrictCoordinate:
    __slots__ = ("_x", "_y")

    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)
```

---

## 🛠️ The Practical Projects

| Project | Description | Encapsulation Techniques Demonstrated |
| :--- | :--- | :--- |
| **1. Secure Bank Account** | Complete transactional ledger system with deposit, withdrawal, and audit histories. | Private balance & PIN hash, defensive copying for ledger statements, validation against overdrafts and invalid credentials. |
| **2. Employee Payroll Engine** | Enterprise compensation system with progressive tax calculation and merit bonuses. | Protected employee IDs, calculated read-only gross pay & tax brackets, validated performance ratings (1.0 - 5.0). |
| **3. User Authentication Vault** | Cryptographic authentication manager with rate-limiting and temporary account lockouts. | Salted SHA-256 hashing, private attempt counter, automatic 3-strike lockout, read-only token issuance. |

---

## 🚀 How to Run the Scripts

Execute any of the scripts using Python 3:

```bash
# 1. Fundamentals: Public, Protected, and Private demonstration
python 01_encapsulation_fundamentals.py

# 2. Name Mangling: In-depth inspect of __dict__, dir(), and inheritance safety
python 02_name_mangling_deep_dive.py

# 3. Getters, Setters & Properties: Validation, computed fields, and deleters
python 03_getters_setters_and_properties.py

# 4. Advanced Safety: Defensive copying, slots, and workflow orchestration
python 04_advanced_encapsulation_and_safety.py

# 5. Production Projects: Bank account, Payroll engine, and Auth vault
python 05_practical_projects.py
```

---

## 💡 Best Practices & Mental Model

1. **Default to Public, Protect when Needed**: Start with simple, clean public attributes. Only introduce properties and private markers when encapsulation or validation is required.
2. **Use Single Underscore `_` for Internal APIs**: Prefer `_attribute` for internal implementation details. It adheres to standard Python idiomatic practice.
3. **Reserve Double Underscore `__` for Collision Avoidance**: Use `__attribute` when building reusable class hierarchies where subclasses might accidentally overwrite internal state.
4. **Never Create Custom Dunders**: Identifiers like `__my_func__` are reserved for Python's language core.
5. **Always Defensively Copy Mutable Structures**: If exposing a list or dictionary from a getter, return a copy or an immutable container (`tuple`, `frozenset`).
6. **"Consenting Adults"**: Encapsulation in Python is an architectural contract for code quality and maintainability, not an impenetrable digital fortress.
