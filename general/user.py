import general_handlers

class User:

    def __init__(self, user_id, username, email, accounts):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.accounts = accounts


    @classmethod
    async def create_new_user(cls, username, email):
        # This should be the value from 'INSERT INTO user (...) VALUES(...) RETURNING user_id'
        return cls(await general_handlers.create_new_user(username, email), username, email, [])