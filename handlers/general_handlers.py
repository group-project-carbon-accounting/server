import json
from general_handler_error import *
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

URL = '127.0.0.1:8888'


async def async_fetch(function, url_suffix, request_dict):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + url_suffix, method='POST', body=json.dumps(request_dict)))
    data = json.loads(response.body)
    if data['status_code'] != 0:
        raise STATUS_CODE_ERROR_DICTIONARY[data['status_code']](function, request_dict)
    return data


async def create_new_user(username, email):
    data = await async_fetch(create_new_user, '/user/create', {
        'username': username,
        'email': email
    })
    return data['user_id']


async def create_new_account(user, account_type):
    data = await async_fetch(create_new_user, '/account/create', {
        'user': user,
        'account_type': account_type
    })
    return data['account_id']


async def add_cash_transaction(account_id, amount, timestamp, vendor):
    data = await async_fetch(create_new_user, '/transaction/add_cash', {
        'account_id': account_id,
        'amount': amount,
        'timestamp': timestamp,
        'vendor': vendor
    })
    return data['transaction_id']


async def add_footprint_transaction(footprint_account_id, footprint, timestamp, associated_transaction_id,
                                    input_method, confidence):
    data = await async_fetch(create_new_user, '/transaction/add_footprint', {
        'footprint_account_id': footprint_account_id,
        'footprint': footprint,
        'timestamp': timestamp,
        'associated_transaction_id': associated_transaction_id,
        'input_method': input_method,
        'confidence': confidence
    })
    return data['transaction_id']


async def add_offset_transaction(offset_account_id, offset, timestamp, offset_cost, offset_method):
    data = await async_fetch(create_new_user, '/transaction/add_offset', {
        'offset_account_id': offset_account_id,
        'offset': offset,
        'timestamp': timestamp,
        'offset_cost': offset_cost,
        'offset_method': offset_method,
    })
    return data['transaction_id']


async def refine_footprint_transaction(transaction_id, footprint, input_method, confidence):
    await async_fetch(create_new_user, '/transaction/refine_footprint', {
        'transaction_id': transaction_id,
        'footprint': footprint,
        'input_method': input_method,
        'confidence': confidence
    })

async def get_associated_footprint_account_id(account_id):
    data = await async_fetch(get_associated_footprint_account_id, '/account/get_associated_footprint_account_id', {
        'account_id': account_id
    })
    return data['account_id']

