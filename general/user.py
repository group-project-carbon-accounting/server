import uuid


class User:

    def __init__(self, user_id, username, email, accounts):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.accounts = accounts

    def add_account(self, account_class):
        """
        Add a new, empty account of the specified account class to the user assuming that all the user's accounts have been included in the list.
        :param :class:`account.Account` account_class: the class of account to be added
        :return: None
        """
        self.accounts.append(account_class.create_new_account(len(self.accounts)))

    @classmethod
    def create_new_user(cls, username, email):
        return cls(uuid.uuid4().int, username, email, [])