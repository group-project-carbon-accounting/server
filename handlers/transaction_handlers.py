import json
import time
import tornado.web, tornado.ioloop
from async_fetch import async_fetch, GET, POST

class TransactionGetHandler(tornado.web.RequestHandler):
    async def get(self, transaction_id):
        response_data = await async_fetch('/purchase/get/' + transaction_id, GET)

        data = {
            'transaction_id': response_data['id'],
            'price': response_data['price'],
            'carbon_cost_offset': response_data['carbon_cost'],
            'vendor': response_data['selr_id'],
            'timestamp': response_data['ts']
        }
        self.write(json.dumps(data))


class TransactionGetRecentHandler(tornado.web.RequestHandler):
    async def get(self, user_id, num_of_days):

        # add 60 seconds just in case of high latency
        ts_now = int(time.time()) + 60
        ts_past = ts_now - int(num_of_days) * 86400 if int(num_of_days) != 0 else 0
        response_data = await async_fetch('/entity/purchases/get/' + user_id + '?start_ts=' + str(ts_past) +
                                          '&end_ts=' + str(ts_now), GET)
        data = {
            'carbon_cost': 0,
            'carbon_offset': 0,
            'transactions': []
        }
        for purchase in response_data['purchase_list']:
            c = purchase['carbon_cost']
            if c >= 0:
                data['carbon_cost'] += c
            else:
                data['carbon_offset'] += c
            data['transactions'].append({
                'transaction_id': purchase['id'],
                'price': purchase['price'],
                'carbon_cost_offset': purchase['carbon_cost'],
                # TODO: query database to see what's the name of the vendor corresponding to that selr_id
                'vendor': purchase['selr_id'],
                'timestamp': int(purchase['ts'])
            })
        self.write(json.dumps(data))


class TransactionUpdateHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)
        # if the old or updated value is negative, then abort
        if request_data['carbon_cost_offset'] < 0:
            self.write(json.dumps({'success': False}))
        transaction_data = await async_fetch('/purchase/get/' + str(request_data['transaction_id']), GET)
        if transaction_data['carbon_cost'] < 0:
            self.write(json.dumps({'success': False}))
        else:
            transaction_data['prch_id'] = request_data['transaction_id']
            transaction_data['carbon_cost'] = request_data['carbon_cost_offset']
            await async_fetch('/purchase/update', POST, data=transaction_data)
            self.write(json.dumps({'success': True}))