import general_handlers

UNKNOWN_FOOTPRINT = 2147483647 # 2^31 - 1

class Transaction:
    def __init__(self, transaction_id, amount, date_time):
        self.transaction_id = transaction_id
        self.amount = amount
        self.date_time = date_time


class CashTransaction(Transaction):
    def __init__(self, transaction_id, amount, date_time, vendor):
        super().__init__(transaction_id, amount, date_time)
        self.vendor = vendor


class FootprintTransaction(Transaction):
    def __init__(self, transaction_id, footprint, date_time, associated_transaction_id, input_method, confidence):
        super().__init__(transaction_id, footprint, date_time)
        self.associated_transaction_id = associated_transaction_id
        self.input_method = input_method
        self.confidence = confidence

    async def refine_footprint(self, footprint, input_method, confidence):
        """
        This function will only update the carbon footprint of the transaction if the confidence associated with the new footprint (possibly dependent on the input method) is greater than the confidence of the old footprint.

        A confidence of zero would indicate that the footprint is obtained from some generic uniform distribution.
        :param int footprint: updated footprint
        :param int input_method: method through which the updated footprint was generated. Assume the integer associated with the method has been registered first in a database table where it is the primary key, among other attributes.
        :param int confidence: confidence of the updated footprint
        :return bool: whether the footprint has been updated
        """
        if confidence > self.confidence:
            await general_handlers.refine_footprint_transaction(self.transaction_id, footprint, input_method, confidence)
            self.amount = footprint
            self.input_method = input_method
            self.confidence = confidence
            return True
        return False


class OffsetTransaction(Transaction):
    def __init__(self, transaction_id, offset, date_time, offset_cost, offset_method):
        super().__init__(transaction_id, offset, date_time)
        self.offset_cost = offset_cost
        self.offset_method = offset_method