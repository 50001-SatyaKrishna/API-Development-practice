class Calculator:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class InsufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InsufficientFunds("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

    def collect_interest(self):
        return self.balance * 0.10
