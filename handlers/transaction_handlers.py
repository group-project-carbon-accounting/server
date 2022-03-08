import asyncio
import datetime
import json
import time
import tornado.web, tornado.ioloop
from handlers.async_fetch import async_fetch, GET, POST, async_get_product_data, async_get_product_info
from handlers.offset_handlers import OFFSET_OPTIONS

class TransactionGetHandler(tornado.web.RequestHandler):
    async def get(self, transaction_id):
        response_data = await async_fetch('/purchase/get/' + transaction_id, GET)

        products = []
        if response_data['item_list']:
            if response_data['carbon_cost'] < 0:
                products.append({'company_name': next(offset_option[1] for offset_option in OFFSET_OPTIONS
                                                      if offset_option[0] == response_data['selr_id']),
                                 'product_name': 'carbon offset'})
            else:
                product_tasks = [asyncio.create_task(async_get_product_info(ids, products))
                                 for ids in response_data['item_list']]
                try:
                    await asyncio.gather(*product_tasks)
                except Exception:
                    for task in product_tasks:
                        task.cancel()
                    self.write(json.dumps({'timestamp': 0}))
                    return

        data = {
            'price': response_data['price'],
            'carbon_cost_offset': response_data['carbon_cost'],
            'vendor': (await async_fetch('/entity/get/' + str(response_data['selr_id']), GET))['display_name'],
            'timestamp': datetime.datetime.fromtimestamp(response_data['ts']).strftime('%a, %d %b %Y, %H:%M:%S'),
            'products': products
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
                # TODO: change this into a list of tasks
                'vendor': (await async_fetch('/entity/get/' + str(purchase['selr_id']), GET))['display_name'],
                'timestamp': datetime.datetime.fromtimestamp(purchase['ts']).strftime('%a, %e %b %Y, %H:%M:%S')
            })
        self.write(json.dumps(data))


class TransactionUpdateHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)
        # if the old or updated value is negative, then abort
        if request_data['carbon_cost_offset'] < 0:
            self.write(json.dumps({'success': False}))
        else:
            transaction_data = await async_fetch('/purchase/get/' + str(request_data['transaction_id']), GET)
            if transaction_data['carbon_cost'] < 0:
                self.write(json.dumps({'success': False}))
            else:
                transaction_data['prch_id'] = request_data['transaction_id']
                old_carbon_cost = transaction_data['carbon_cost']
                transaction_data['carbon_cost'] = request_data['carbon_cost_offset']
                response_data = await async_fetch('/purchase/update', POST, data=transaction_data)

                if response_data['status'] != 'success':
                    self.write(json.dumps({'success': False}))
                else:
                    # this is successful whether the entity was updated or not, since the transaction has already been updated
                    # and transactions are the canonical records. Again, the redundant data in entity may be out of sync.
                    self.write(json.dumps({'success': True}))

                    # TODO: fix concurrency issue; if transactions are concurrent, then race conditions can occur,
                    #       and the carbon cost and offset value can be different from the sum of transactions as in
                    #       TransactionGetRecentHandler

                    response_data_1 = await async_fetch('/entity/get/' + str(transaction_data['buyr_id']), GET)
                    response_data_1['carbon_cost'] += (request_data['carbon_cost_offset'] - old_carbon_cost)
                    await async_fetch('/entity/update', POST, data=response_data_1)


class TransactionUpdateProductsHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)
        transaction_data = await async_fetch('/purchase/get/' + str(request_data['transaction_id']), GET)

        if transaction_data['carbon_cost'] < 0:
            self.write(json.dumps({'success': False}))
        else:
            carbon_cost = [0]
            product_tasks = [asyncio.create_task(async_get_product_data(product, carbon_cost))
                             for product in request_data['products']]
            try:
                # if any product is an offsetting one, raise Exception
                await asyncio.gather(*product_tasks)
            except Exception:
                for task in product_tasks:
                    task.cancel()
                self.write(json.dumps({'success': False}))
            else:
                products = [{'prod_id': product['product_id'], 'comp_id': product['company_id']}
                            for product in request_data['products']]
                transaction_data['item_list'] = products
                old_carbon_cost = transaction_data['carbon_cost']
                transaction_data['carbon_cost'] = carbon_cost[0]
                transaction_data['prch_id'] = transaction_data['id']
                del(transaction_data['id'])
                response_data = await async_fetch('/purchase/update', POST, data=transaction_data)
                if response_data['status'] != 'success':
                    self.write(json.dumps({'success': False}))
                else:
                    self.write(json.dumps({'success': True}))

                    response_data_1 = await async_fetch('/entity/get/' + str(transaction_data['buyr_id']), GET)
                    response_data_1['carbon_cost'] += (carbon_cost[0] - old_carbon_cost)
                    await async_fetch('/entity/update', POST, data=response_data_1)

