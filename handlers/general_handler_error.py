
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

STATUS_CODE_ERROR_DICTIONARY = {
    1 : DatabaseTransactionError,
    2 : InsufficientFundError,
    3 : MoreThanOneFootprintOrOffsetAccountError
}