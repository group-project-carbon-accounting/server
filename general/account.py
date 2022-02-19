import general_handlers
import enum

class AccountType(enum.Enum):
    CASH = 0,
    FOOTPRINT = 1,
    OFFSET = 2

class Account:

    def __init__(self, account_id, balance, transactions):
        self.account_id = account_id
        self.balance = balance
        self.transactions = transactions

    @classmethod
    async def create_new_account(cls, user, account_type: AccountType):
        # This should be the value from 'INSERT INTO account (...) VALUES(...) RETURNING account_id'
        return cls(await general_handlers.create_new_account(user, account_type), 0, [])