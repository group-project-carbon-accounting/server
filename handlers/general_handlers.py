import json
import general_handler_error
import timestamp
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

URL = '127.0.0.1:8888'


async def async_fetch(function, url_suffix, request_json):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + url_suffix, method='POST', body=request_json))
    data = response.headers
    # the status code must be included in the header of the response
    if data['status_code'] != 0:
        raise general_handler_error.STATUS_CODE_ERROR_DICTIONARY[data['status_code']](function, request_json)
    return response.body


async def create_new_user(username, email):
    return await create_new_user_json({
        'username': username,
        'email': email
    })

async def create_new_account(user_id, account_type):
    return await create_new_account_json(json.dumps({
        'user_id': user_id,
        'account_type': account_type
    }))

async def add_cash_transaction(account_id, amount, timestamp, vendor):
    return await add_cash_transaction_json(json.dumps({
        'account_id': account_id,
        'amount': amount,
        'timestamp': timestamp,
        'vendor': vendor
    }))

async def add_footprint_transaction(footprint_account_id, footprint, timestamp, associated_transaction_id,
                                    input_method, confidence):
    return await add_footprint_transaction_json(json.dumps({
        'footprint_account_id': footprint_account_id,
        'footprint': footprint,
        'timestamp': timestamp,
        'associated_transaction_id': associated_transaction_id,
        'input_method': input_method,
        'confidence': confidence
    }))

async def add_offset_transaction(offset_account_id, offset, timestamp, offset_cost, offset_method):
    return await add_offset_transaction_json(json.dumps({
        'offset_account_id': offset_account_id,
        'offset': offset,
        'timestamp': timestamp,
        'offset_cost': offset_cost,
        'offset_method': offset_method,
    }))

async def refine_footprint_transaction(transaction_id, footprint, input_method, confidence):
    return await refine_footprint_transaction_json(json.dumps({
        'transaction_id': transaction_id,
        'footprint': footprint,
        'input_method': input_method,
        'confidence': confidence
    }))

async def get_associated_footprint_account_id(account_id):
    return await get_associated_footprint_account_id_json(json.dumps({
        'account_id': account_id
    }))

async def get_recent_transactions(account_id, number_of_days):
    # ignore leap second nonsense
    return await get_recent_transactions_json(json.dumps({
        'account_id': account_id,
        'timestamp': timestamp.generate_timestamp() - 86400 * number_of_days,
    }))

async def create_new_user_json(json_):
    return await async_fetch(create_new_user_json, '/user/create', json_)

async def create_new_account_json(json_):
    return await async_fetch(create_new_account_json, 'account/create', json_)

async def add_cash_transaction_json(json_):
    return await async_fetch(add_cash_transaction_json, '/transaction/add_cash', json_)

async def add_footprint_transaction_json(json_):
    return await async_fetch(add_footprint_transaction_json, '/transaction/add_footprint', json_)

async def add_offset_transaction_json(json_):
    return await async_fetch(add_offset_transaction_json, '/transaction/add_offset', json_)

async def refine_footprint_transaction_json(json_):
    return await async_fetch(refine_footprint_transaction_json, '/transaction/refine_footprint', json_)

async def get_associated_footprint_account_id_json(json_):
    return await async_fetch(get_associated_footprint_account_id_json, '/account/get_associated_footprint_account_id', json_)

# should use the non-json version to calculate the timestamp
async def get_recent_transactions_json(json_):
    return await async_fetch(get_recent_transactions_json, 'transaction/get_recent', json_)