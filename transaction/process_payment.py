import asyncio
import general_handlers
import general_handler_error
import timestamp

async def process_payment(account_id, amount, vendor):
    try:
        transaction_id = await general_handlers.add_cash_transaction(account_id, amount, timestamp.generate_timestamp(), vendor)
    except general_handler_error.GeneralHandlerError as e:
        return str(e)
    else:
        return transaction_id

async def process_payment_with_footprint(account_id, amount, vendor, footprint, confidence):
    try:
        timestamp_ = timestamp.generate_timestamp()
        cash_transaction_id = asyncio.create_task(general_handlers.add_cash_transaction(account_id, amount, timestamp, vendor))
        footprint_account_id = asyncio.create_task(general_handlers.get_associated_footprint_account_id(account_id))
        await cash_transaction_id
        await footprint_account_id
    except general_handler_error.GeneralHandlerError as e:
        return str(e)
    else:
        # TODO: change input_method to dictionary in input_footprint
        # TODO: return status code, and call a blackbox payment function
        try:
            footprint_transaction_id = await general_handlers.add_footprint_transaction(footprint_account_id, footprint, timestamp_, cash_transaction_id, 0, confidence)
        except general_handler_error.GeneralHandlerError as e:
            return str(e)
        else:
            return cash_transaction_id