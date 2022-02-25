import json
import time
import tornado.web, tornado.ioloop
from async_fetch import async_fetch, GET, POST


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
        if request_data['carbon_cost'] < 0:
            self.write(json.dumps({'success': False}))
        transaction_data = await async_fetch('/purchase/get/' + str(request_data['transaction_id']), GET)
        if transaction_data['carbon_cost'] < 0:
            self.write(json.dumps({'success': False}))
        else:
            transaction_data['prch_id'] = request_data['transaction_id']
            transaction_data['carbon_cost'] = request_data['carbon_cost']
            await async_fetch('/purchase/update', POST, data=transaction_data)
            self.write(json.dumps({'success': True}))


# TODO: move this to separate test module
app = tornado.web.Application([
        ('/transaction/get_recent/(?P<user_id>[0-9]+)/(?P<num_of_days>[0-9]+)', TransactionGetRecentHandler),
        ('/transaction/update', TransactionUpdateHandler),
    ])

if __name__ == '__main__':
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()