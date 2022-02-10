class Account:

    def __init__(self, user_id, account_number, balance):
        self.user_id = user_id
        self.account_number = account_number
        self.balance = balance

    @classmethod
    def create_new_account(cls, user):
        return cls(user.user_id, len(user.accounts), 0)

class CreditAccount(Account):
    pass

class CarbonAccount(Account):
    pass