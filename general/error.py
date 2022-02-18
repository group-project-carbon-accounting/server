
class DatabaseTransactionError(Exception):

    def __init__(self, transaction):
        self.transaction = transaction.__name__

    def __str__(self):
        return str(self.transaction)