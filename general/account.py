class Account:

    def __init__(self, account_number, balance, transactions):
        self.account_number = account_number
        self.balance = balance
        self.transactions = transactions

    @classmethod
    def create_new_account(cls, account_number):
        return cls(account_number, 0, [])

class CreditAccount(Account):
    pass

class CarbonAccount(Account):
    pass