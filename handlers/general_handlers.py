import requests

URL = '127.0.0.1:8888'

def create_new_user(username, email):
    r = requests.post(URL + r'/user/create', data={'username': username, 'email': email})
    return int(r.content)

def create_new_account(user):
    r = requests.post(URL + r'/account/create', data={'user': user})
    return int(r.content)

def add_transaction(transaction_id, amount, vendor, date_time, carbon_footprint, input_method, confidence):
    # update both account balance and create new transaction
    r = requests.post(URL + r'/transaction/add', data={'transaction_id': transaction_id,
                                                       'amount': amount,
                                                       'vendor': vendor,
                                                       'date_time': date_time,
                                                       'carbon_footprint': carbon_footprint,
                                                       'input_method': input_method,
                                                       'confidence': confidence})

def refine_transaction_footprint(transaction_id, carbon_footprint, input_method, confidence):
    r = requests.post(URL + r'/transaction/update', data ={'transaction_id': transaction_id,
                                                           'carbon_footprint': carbon_footprint,
                                                           'input_method': input_method,
                                                           'confidence': confidence})