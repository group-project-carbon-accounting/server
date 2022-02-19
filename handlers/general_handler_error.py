
class GeneralHandlerError(Exception):
    def __init__(self, function, request_dict):
        self.function = function
        self.request_dict = request_dict

class DatabaseTransactionError(GeneralHandlerError):
    pass

class InsufficientFundError(GeneralHandlerError):
    pass

class MoreThanOneFootprintOrOffsetAccountError(GeneralHandlerError):
    pass

class NotFootprintTransactionRefinedError(GeneralHandlerError):
    pass

class InvalidTimestampError(GeneralHandlerError):
    pass

STATUS_CODE_ERROR_DICTIONARY = {
    1 : DatabaseTransactionError,
    2 : InsufficientFundError,
    3 : MoreThanOneFootprintOrOffsetAccountError,
    4 : NotFootprintTransactionRefinedError,
    5 : InvalidTimestampError,
}

ERROR_STATUS_CODE_DICTIONARY = {v: k for k, v in STATUS_CODE_ERROR_DICTIONARY.items()}