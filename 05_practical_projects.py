"""
================================================================================
Day 20: Python Object-Oriented Programming - Production Practical Projects
================================================================================
This script synthesizes all core and advanced encapsulation concepts into
three comprehensive, industry-grade projects:

Project 1: Secure Digital Banking System with Transaction Auditing
Project 2: Enterprise Employee Compensation & Tax Calculation Engine
Project 3: User Authentication Vault with Rate-Limiting & Salting
================================================================================
"""

import hashlib
import secrets
from datetime import datetime
from typing import List, Tuple, Dict, Any


def print_separator(title: str):
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


# ==============================================================================
# PROJECT 1: SECURE DIGITAL BANKING SYSTEM
# ==============================================================================
# Demonstrates:
# - Private balance and private hashed PIN
# - Defensive copying on transaction records
# - Business validation on all deposits, withdrawals, and transfers
# - Read-only transaction ledger access

class SecureBankAccount:
    def __init__(self, account_number: str, holder_name: str, initial_deposit: float, pin: str):
        if not account_number or len(account_number) < 5:
            raise ValueError("Account number must be at least 5 characters.")
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        if len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be a 4-digit numeric string.")

        self.account_number = account_number          # Public
        self.holder_name = holder_name                # Public
        self._account_created_at = datetime.now()     # Protected
        self.__balance = float(initial_deposit)       # Private
        self.__pin_hash = self.__hash_pin(pin)        # Private hashed PIN
        self.__transactions = []                      # Private mutable ledger

        # Record initial funding
        self.__log_transaction("INITIAL_DEPOSIT", initial_deposit, "Account opened")

    # Private helper for PIN hashing
    @staticmethod
    def __hash_pin(pin: str) -> str:
        return hashlib.sha256(pin.encode("utf-8")).hexdigest()

    # Private helper to log transactions
    def __log_transaction(self, tx_type: str, amount: float, note: str):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": tx_type,
            "amount": amount,
            "balance_after": self.__balance,
            "note": note,
        }
        self.__transactions.append(record)

    def verify_pin(self, candidate_pin: str) -> bool:
        """Controlled public interface to check authentication."""
        return self.__hash_pin(candidate_pin) == self.__pin_hash

    # Read-only property for balance (requires PIN verification)
    def check_balance(self, pin: str) -> float:
        if not self.verify_pin(pin):
            raise PermissionError("Access Denied: Invalid 4-digit PIN provided.")
        return self.__balance

    # Defensive copy property for transaction statement
    def get_statement(self, pin: str) -> Tuple[Dict[str, Any], ...]:
        if not self.verify_pin(pin):
            raise PermissionError("Access Denied: Invalid 4-digit PIN provided.")
        # Return tuple of copies to prevent caller from mutating internal history
        return tuple(dict(record) for record in self.__transactions)

    def deposit(self, amount: float, note: str = "Deposit") -> bool:
        if amount <= 0:
            raise ValueError("Deposit amount must be strictly greater than $0.00.")
        self.__balance += amount
        self.__log_transaction("CREDIT", amount, note)
        print(f"[+] Deposit successful: +${amount:.2f} | New Balance: ${self.__balance:.2f}")
        return True

    def withdraw(self, amount: float, pin: str, note: str = "Withdrawal") -> bool:
        if not self.verify_pin(pin):
            print("[-] Withdrawal Rejected: Authentication failure.")
            return False
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly greater than $0.00.")
        if amount > self.__balance:
            print(f"[-] Withdrawal Rejected: Insufficient funds (Available: ${self.__balance:.2f}).")
            return False

        self.__balance -= amount
        self.__log_transaction("DEBIT", amount, note)
        print(f"[+] Withdrawal successful: -${amount:.2f} | Remaining Balance: ${self.__balance:.2f}")
        return True

    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        if not self.verify_pin(old_pin):
            raise PermissionError("Cannot change PIN: Old PIN is incorrect.")
        if len(new_pin) != 4 or not new_pin.isdigit():
            raise ValueError("New PIN must be a 4-digit numeric string.")
        self.__pin_hash = self.__hash_pin(new_pin)
        self.__log_transaction("PIN_CHANGE", 0.0, "Security credential updated")
        print("[+] Security PIN successfully updated.")
        return True


# ==============================================================================
# PROJECT 2: ENTERPRISE EMPLOYEE & PAYROLL SYSTEM
# ==============================================================================
# Demonstrates:
# - Protected employee ID and base salary
# - Computed properties: gross annual pay, tax brackets, net monthly pay
# - Property setter with bounded validation on performance rating (1.0 - 5.0)
# - Encapsulated salary revision with automatic audit logging

class EmployeeRecord:
    # Tax brackets: (threshold, marginal_rate)
    TAX_BRACKETS = (
        (50000, 0.10),
        (100000, 0.20),
        (float("inf"), 0.30),
    )

    def __init__(self, emp_id: str, full_name: str, department: str, base_monthly_salary: float):
        self._emp_id = emp_id                              # Protected
        self.full_name = full_name                         # Public
        self.department = department                       # Public
        self._base_monthly_salary = float(base_monthly_salary)  # Protected
        self._performance_rating = 3.0                     # Protected (default average)
        self._audit_log = []

        self._record_audit(f"Employee profile initialized with base salary ${base_monthly_salary:.2f}")

    def _record_audit(self, event: str):
        self._audit_log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")

    @property
    def emp_id(self) -> str:
        """Read-only employee ID."""
        return self._emp_id

    @property
    def performance_rating(self) -> float:
        """Performance score getter."""
        return self._performance_rating

    @performance_rating.setter
    def performance_rating(self, score: float):
        """Setter with strict validation between 1.0 and 5.0."""
        if not isinstance(score, (int, float)):
            raise TypeError("Performance score must be a number.")
        if not (1.0 <= score <= 5.0):
            raise ValueError(f"Performance score must be between 1.0 and 5.0, got {score}.")
        old_score = self._performance_rating
        self._performance_rating = float(score)
        self._record_audit(f"Performance rating updated from {old_score} to {self._performance_rating}")
        print(f"[+] Performance rating updated to {self._performance_rating}/5.0")

    @property
    def performance_bonus_multiplier(self) -> float:
        """Derived bonus multiplier based on rating."""
        if self._performance_rating >= 4.5:
            return 0.20  # 20% bonus
        elif self._performance_rating >= 3.5:
            return 0.10  # 10% bonus
        elif self._performance_rating >= 2.5:
            return 0.05  # 5% bonus
        return 0.0      # No bonus

    @property
    def annual_gross_compensation(self) -> float:
        """Read-only computed gross annual compensation including performance bonus."""
        base_annual = self._base_monthly_salary * 12
        bonus = base_annual * self.performance_bonus_multiplier
        return base_annual + bonus

    @property
    def estimated_annual_tax(self) -> float:
        """Computed progressive tax liability."""
        gross = self.annual_gross_compensation
        tax = 0.0
        taxable_prev = 0.0

        for limit, rate in self.TAX_BRACKETS:
            if gross > limit:
                taxable_chunk = limit - taxable_prev
                tax += taxable_chunk * rate
                taxable_prev = limit
            else:
                taxable_chunk = gross - taxable_prev
                tax += taxable_chunk * rate
                break
        return tax

    @property
    def net_monthly_take_home(self) -> float:
        """Computed estimated net take home per month."""
        net_annual = self.annual_gross_compensation - self.estimated_annual_tax
        return net_annual / 12

    def adjust_base_salary(self, percentage_raise: float):
        """Safe method to adjust salary with verification."""
        if percentage_raise < -20.0 or percentage_raise > 50.0:
            raise ValueError("Salary adjustments must be between -20% and +50% per cycle.")
        old_salary = self._base_monthly_salary
        self._base_monthly_salary *= (1 + percentage_raise / 100)
        self._record_audit(
            f"Salary changed by {percentage_raise:+0.1f}%: ${old_salary:.2f} -> ${self._base_monthly_salary:.2f}"
        )
        print(f"[+] Base monthly salary updated to ${self._base_monthly_salary:.2f}")

    def generate_paystub_summary(self) -> str:
        return (
            f"--- Paystub Summary: {self.full_name} ({self._emp_id}) ---\n"
            f"Department: {self.department}\n"
            f"Base Monthly: ${self._base_monthly_salary:,.2f}\n"
            f"Performance Rating: {self._performance_rating}/5.0 (Bonus: +{self.performance_bonus_multiplier * 100:.0f}%)\n"
            f"Annual Gross: ${self.annual_gross_compensation:,.2f}\n"
            f"Estimated Annual Tax: ${self.estimated_annual_tax:,.2f}\n"
            f"Estimated Net Monthly: ${self.net_monthly_take_home:,.2f}\n"
        )


# ==============================================================================
# PROJECT 3: USER AUTHENTICATION VAULT
# ==============================================================================
# Demonstrates:
# - Salted password hashing (preventing rainbow table attacks)
# - Account lockout mechanism after 3 consecutive failed attempts
# - Read-only authentication tokens
# - Method encapsulation for internal security operations

class UserCredentialVault:
    MAX_ATTEMPTS = 3

    def __init__(self, username: str, raw_password: str):
        if len(username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(raw_password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        self.username = username.strip()               # Public
        self._salt = secrets.token_hex(16)             # Protected salt
        self.__password_hash = self.__hash(raw_password, self._salt) # Private hash
        self.__failed_attempts = 0                     # Private counter
        self.__is_locked = False                       # Private state
        self.__active_session_token = None             # Private token

    def __hash(self, password: str, salt: str) -> str:
        """Internal private method: SHA-256 with cryptographic salt."""
        payload = f"{salt}:{password}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @property
    def is_locked(self) -> bool:
        """Read-only property exposing lock status."""
        return self.__is_locked

    @property
    def failed_attempts(self) -> int:
        return self.__failed_attempts

    def authenticate(self, candidate_password: str) -> str:
        """
        Validates password and returns an active session token if valid.
        Increments failed attempts and triggers lockout if max attempts exceeded.
        """
        if self.__is_locked:
            raise PermissionError("ACCOUNT LOCKED: Exceeded maximum allowed login attempts.")

        candidate_hash = self.__hash(candidate_password, self._salt)
        if candidate_hash == self.__password_hash:
            # Reset failures upon success
            self.__failed_attempts = 0
            self.__active_session_token = secrets.token_hex(24)
            print(f"[+] Authentication successful for '{self.username}'!")
            return self.__active_session_token
        else:
            self.__failed_attempts += 1
            remaining = self.MAX_ATTEMPTS - self.__failed_attempts
            print(f"[-] Authentication failed! {remaining} attempts remaining.")
            if self.__failed_attempts >= self.MAX_ATTEMPTS:
                self.__is_locked = True
                print(f"[!] SECURITY ALERT: Account '{self.username}' has been LOCKED due to failed logins.")
            raise ValueError("Invalid password.")

    def reset_lock(self, admin_key: str):
        """Admin recovery override to unlock the account."""
        if admin_key != "SUPER_ADMIN_MASTER_KEY_2026":
            raise PermissionError("Unauthorized admin override key.")
        self.__is_locked = False
        self.__failed_attempts = 0
        print(f"[+] Account '{self.username}' unlocked by administrator.")


# ==============================================================================
# DEMONSTRATION & RUNNER
# ==============================================================================
if __name__ == "__main__":
    # --- DEMO 1: Secure Bank Account ---
    print_separator("PROJECT 1 DEMO: Secure Bank Account & Transaction Ledger")
    acc = SecureBankAccount("AC-88392", "Sameer Mohammed", 2500.0, "4810")
    print(f"Account: {acc.account_number} | Owner: {acc.holder_name}")

    acc.deposit(1200.0, "Freelance payment")
    acc.withdraw(500.0, "4810", "Groceries & Utilities")
    acc.withdraw(8000.0, "4810", "New car downpayment")  # Insufficient funds

    print("\nRetrieving Statement with valid PIN:")
    for tx in acc.get_statement("4810"):
        print(f"  [{tx['timestamp']}] {tx['type']:<15} ${tx['amount']:>8.2f} | Balance: ${tx['balance_after']:>8.2f} ({tx['note']})")

    # --- DEMO 2: Employee Payroll System ---
    print_separator("PROJECT 2 DEMO: Enterprise Employee Payroll Engine")
    emp = EmployeeRecord("EMP-1042", "Sameer Mohammed", "Engineering", 6500.0)
    print(emp.generate_paystub_summary())

    print("[Performance Review & Promotion Cycle]:")
    emp.performance_rating = 4.8  # Top tier rating triggers 20% bonus
    emp.adjust_base_salary(15.0)  # 15% raise
    print()
    print(emp.generate_paystub_summary())

    # --- DEMO 3: User Authentication Vault ---
    print_separator("PROJECT 3 DEMO: User Authentication & Security Vault")
    vault = UserCredentialVault("sameer_admin", "MasterSecureKey2026!")

    print("[1] Attempting authentication with incorrect password:")
    try:
        vault.authenticate("wrong_pass_1")
    except ValueError:
        pass

    print("\n[2] Attempting second failed login:")
    try:
        vault.authenticate("wrong_pass_2")
    except ValueError:
        pass

    print("\n[3] Attempting third failed login (triggers lock):")
    try:
        vault.authenticate("wrong_pass_3")
    except ValueError:
        pass

    print(f"\nIs account locked? -> {vault.is_locked}")

    print("\n[4] Attempting login while locked (even with correct password):")
    try:
        vault.authenticate("MasterSecureKey2026!")
    except PermissionError as err:
        print(f"[!] Access Refused: {err}")

    print("\n[5] Administrator resets lock and user logs in successfully:")
    vault.reset_lock("SUPER_ADMIN_MASTER_KEY_2026")
    token = vault.authenticate("MasterSecureKey2026!")
    print(f"Issued Session Token: {token[:12]}... (Length: {len(token)})")
