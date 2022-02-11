import general_handlers

class Account:

    def __init__(self, account_number, balance, transactions):
        self.account_number = account_number
        self.balance = balance
        self.transactions = transactions

    @classmethod
    def create_new_account(cls, user):
        # This should be the value from 'INSERT INTO account (...) VALUES(...) RETURNING account_number'
        return cls(general_handlers.create_new_account(user), 0, [])