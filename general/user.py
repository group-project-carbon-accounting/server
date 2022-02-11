from account import Account

class User:

    def __init__(self, user_id, username, email, accounts):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.accounts = accounts

    def add_account(self):
        self.accounts.append(Account.create_new_account())

    @classmethod
    def create_new_user(cls, username, email):
        user_id = 0
        # This should be the value from 'INSERT INTO user (...) VALUES(...) RETURNING user_id'
        return cls(user_id, username, email, [])