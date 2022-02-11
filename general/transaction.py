class Transaction:
    def __init__(self, amount, vendor, date_time):
        self.amount = amount
        self.vendor = vendor
        self.date_time = date_time

class CarbonTransaction(Transaction):

    def __init__(self, amount, vendor, date_time, carbon_footprint, input_method, confidence):
        super().__init__(amount, vendor, date_time)
        self.carbon_footprint = carbon_footprint
        self.input_method = input_method
        self.confidence = confidence

    def refine_transaction_footprint(self, carbon_footprint, input_method, confidence):
        """
        This function will only update the carbon footprint of the transaction if the confidence associated with the new footprint (possibly dependent on the input method) is greater than the confidence of the old footprint.

        A confidence of zero would indicate that the footprint is obtained from some generic uniform distribution.
        :param int carbon_footprint: updated footprint
        :param int input_method: method through which the updated footprint was generated. Assume the integer associated with the method has been registered first in a database table where it is the primary key, among other attributes. 
        :param int confidence: confidence of the updated footprint
        :return bool: whether the footprint has been updated
        """
        if confidence > self.confidence:
            self.carbon_footprint = carbon_footprint
            self.input_method = input_method
            self.confidence = confidence
            return True
        return False