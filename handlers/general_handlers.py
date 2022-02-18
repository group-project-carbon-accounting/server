import json
from error import *
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

URL = '127.0.0.1:8888'
DATABASE_ERROR = 0

async def create_new_user(username, email):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/user/create', method='POST', body=json.dumps({
        'username': username,
        'email': email
    })))
    user_id = json.loads(response.body)['user_id']
    if user_id == DATABASE_ERROR:
        raise DatabaseTransactionError(create_new_account)
    else:
        return user_id


async def create_new_account(user, account_type):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/account/create', method='POST', body=json.dumps({
        'user': user,
        'account_type': account_type
    })))
    account_number = json.loads(response.body)['account_number']
    if account_number == DATABASE_ERROR:
        raise DatabaseTransactionError(create_new_account)
    else:
        return account_number


async def add_cash_transaction(account_number, amount, date_time, vendor):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/transaction/add', method='POST', body=json.dumps({
        'account_number': account_number,
        'amount': amount,
        'date_time': date_time,
        'vendor': vendor
    })))
    transaction_id = json.loads(response.body)['transaction_id']
    if transaction_id == DATABASE_ERROR:
        raise DatabaseTransactionError(add_cash_transaction)
    else:
        return transaction_id


async def add_footprint_transaction(footprint_account_number, footprint, date_time, associated_transaction_id, input_method,
                                    confidence):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(
        HTTPRequest(url=URL + '/transaction/add_footprint', method='POST', body=json.dumps({
            'footprint_account_number': footprint_account_number,
            'footprint': footprint,
            'date_time': date_time,
            'associated_transaction_id': associated_transaction_id,
            'input_method': input_method,
            'confidence': confidence
        })))
    transaction_id = json.loads(response.body)['transaction_id']
    if transaction_id == DATABASE_ERROR:
        raise DatabaseTransactionError(add_footprint_transaction)
    else:
        return transaction_id


async def add_offset_transaction(offset_account_number, offset, date_time, offset_cost, offset_method):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/transaction/add_offset', method='POST', body=json.dumps({
        'offset_account_number': offset_account_number,
        'offset': offset,
        'date_time': date_time,
        'offset_cost': offset_cost,
        'offset_method': offset_method,
    })))
    transaction_id = json.loads(response.body)['transaction_id']
    if transaction_id == DATABASE_ERROR:
        raise DatabaseTransactionError(add_offset_transaction)
    else:
        return transaction_id


async def refine_footprint_transaction(transaction_id, footprint, input_method, confidence):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(
        HTTPRequest(url=URL + '/transaction/refine_footprint', method='POST', body=json.dumps({
            'transaction_id': transaction_id,
            'footprint': footprint,
            'input_method': input_method,
            'confidence': confidence
        })))
    if not json.loads(response.body)['success']:
        raise DatabaseTransactionError(refine_footprint_transaction)