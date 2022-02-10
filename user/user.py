import uuid


class User:

    def __init__(self, user_id, username, email, accounts):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.accounts = accounts

    def add_account(self, account_class):
        self.accounts.append(account_class.create_new_account(self))

    @classmethod
    def create_new_user(cls, username, email):
        return cls(uuid.uuid4().int, username, email, [])