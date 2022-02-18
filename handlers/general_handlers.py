import json

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

URL = '127.0.0.1:8888'


async def create_new_user(username, email):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/user/create', method='POST', body=json.dumps({
        'username': username,
        'email': email
    })))
    return json.loads(response.body)['user_id']


async def create_new_account(user, account_type):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/account/create', method='POST', body=json.dumps({
        'user': user,
        'account_type': account_type
    })))
    return json.loads(response.body)['account_number']


async def add_transaction(account_number, amount, vendor, date_time):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/transaction/add', method='POST', body=json.dumps({
        'account_number': account_number,
        'amount': amount,
        'vendor': vendor,
        'date_time': date_time
    })))
    return json.loads(response.body)['transaction_id']


async def add_footprint_transaction(footprint_account_number, footprint, associated_transaction_id, input_method,
                                    confidence, date_time):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(
        HTTPRequest(url=URL + '/transaction/add_footprint', method='POST', body=json.dumps({
            'footprint_account_number': footprint_account_number,
            'footprint': footprint,
            'associated_transaction_id': associated_transaction_id,
            'input_method': input_method,
            'confidence': confidence,
            'date_time': date_time
        })))
    return json.loads(response.body)['transaction_id']


async def add_offset_transaction(offset_account_number, offset, offset_method, date_time):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + '/transaction/add_offset', method='POST', body=json.dumps({
        'offset_account_number': offset_account_number,
        'offset': offset,
        'offset_method': offset_method,
        'date_time': date_time
    })))
    return json.loads(response.body)['transaction_id']


async def refine_footprint_transaction(footprint_transaction_id, footprint, input_method, confidence):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(
        HTTPRequest(url=URL + '/transaction/refine_footprint', method='POST', body=json.dumps({
            'footprint_transaction_id': footprint_transaction_id,
            'footprint': footprint,
            'input_method': input_method,
            'confidence': confidence
        })))
    return json.loads(response.body)['success']
