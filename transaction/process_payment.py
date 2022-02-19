import asyncio

import general_handlers
import time
from general_handler_error import *

TIMESTAMP_OF_2020 = 1577836800

def generate_timestamp():
    return int(time.time()) - TIMESTAMP_OF_2020

async def process_payment(account_id, amount, vendor):
    try:
        transaction_id = await general_handlers.add_cash_transaction(account_id, amount, generate_timestamp(), vendor)
    except GeneralHandlerError as e:
        return str(e)
    else:
        return transaction_id

async def process_payment(account_id, amount, vendor, footprint, confidence):
    try:
        timestamp = generate_timestamp()
        cash_transaction_id = asyncio.create_task(general_handlers.add_cash_transaction(account_id, amount, timestamp, vendor))
        footprint_account_id = asyncio.create_task(general_handlers.get_associated_footprint_account_id(account_id))
        await cash_transaction_id
        await footprint_account_id
    except GeneralHandlerError as e:
        return str(e)
    else:
        # TODO: change input_method and confidence to dictionary in input_footprint
        # TODO: add 1-to-1 mapping from error code to error
        # TODO: return status code, and call a blackbox payment function
        try:
            footprint_transaction_id = await general_handlers.add_footprint_transaction(footprint_account_id, footprint, timestamp, cash_transaction_id, 0, confidence)
        except GeneralHandlerError as e:
            return str(e)
        else:
            return cash_transaction_id