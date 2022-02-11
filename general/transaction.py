


class Transaction:
    def __init__(self, amount, vendor, date_time):
        self.amount = amount
        self.vendor = vendor
        self.date_time = date_time

class CarbonTransaction(Transaction):

    def __init__(self, amount, vendor, date_time, input_method, confidence):
        super().__init__(amount, vendor, date_time)
        self.input_method = input_method
        self.confidence = confidence

    def refine_transaction_amount(self, amount, input_method, confidence):
        """
        This function will only update the carbon cost of the transaction if the confidence associated with the new amount (possibly dependent on the input method) is greater than the confidence of the old amount.

        A confidence of zero would indicate that the amount is obtained from some generic uniform distribution.
        :param int amount: updated amount
        :param function input_method: method through which the updated amount was generated
        :param int confidence: confidence of the updated amount
        :return bool: whether the amount has been updated
        """
        if confidence > self.confidence:
            self.amount = amount
            self.input_method = input_method
            self.confidence = confidence
            return True
        return False
