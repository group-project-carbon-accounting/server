
class GeneralHandlerError(Exception):
    def __init__(self, function, request_dict):
        self.function = function
        self.request_dict = request_dict

# The database has suffered internal errors or exceptions such that the transaction has failed
class DatabaseTransactionError(GeneralHandlerError):
    pass

# There is insufficient fund in the cash account to carry out the transaction
class InsufficientFundError(GeneralHandlerError):
    pass

# Attempting to create another footprint or offset account
class MoreThanOneFootprintOrOffsetAccountError(GeneralHandlerError):
    pass

# Attempting to refine a non-footprint transaction
class NotFootprintTransactionRefinedError(GeneralHandlerError):
    pass

# The timestamp passed is invalid
class InvalidTimestampError(GeneralHandlerError):
    pass

# There is no associated footprint account
class NoAssociatedFootprintAccountError(GeneralHandlerError):
    pass

STATUS_CODE_ERROR_DICTIONARY = {
    1 : DatabaseTransactionError,
    2 : InsufficientFundError,
    3 : MoreThanOneFootprintOrOffsetAccountError,
    4 : NotFootprintTransactionRefinedError,
    5 : InvalidTimestampError,
    6 : NoAssociatedFootprintAccountError
}

ERROR_STATUS_CODE_DICTIONARY = {v: k for k, v in STATUS_CODE_ERROR_DICTIONARY.items()}