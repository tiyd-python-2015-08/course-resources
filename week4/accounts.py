class OverdrawnException(Exception):
    pass

class BankAccount:
    def __init__(self, account_number, routing_number, balance=0):
        self.account_number = account_number
        self.routing_number = routing_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("You must deposit a positive amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("You must withdraw a positive amount")
        if amount > self.balance:
            raise OverdrawnException("You can't withdraw more than your balance")
        self.balance -= amount


class CheckingAccount(BankAccount):
    pass


class SavingsAccount(BankAccount):
    def __init__(self, account_number, routing_number, balance=0, interest_rate=0):
        super().__init__(account_number, routing_number, balance)
        self.interest_rate = interest_rate
        self.transaction_count = 0

    def compound_interest(self):
        self.balance += (self.interest_rate / 12 * self.balance)

    def withdraw(self, amount):
        self.transaction_count += 1
        super().withdraw(amount)
