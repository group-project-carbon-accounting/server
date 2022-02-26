import asyncio
import json
import tornado.web
from handlers.async_fetch import async_fetch, GET, POST, async_get_offset_options

# TODO: include this as a database table
OFFSET_OPTIONS = [
    (13, 'A blend of offsetting projects'),
    (14, 'Store carbon underground for thousands of years'),
    (15, 'Rebuild the natural habitats'),
    (16, 'Renewable energy for all'),
    (17, 'Reduce global warming by burning methane'),
]
OFFSET_PRODUCT_ID = 12

class OffsetGetHandler(tornado.web.RequestHandler):
    async def get(self):
        offset_tasks = [async_get_offset_options(*offset_option, OFFSET_PRODUCT_ID) for offset_option in OFFSET_OPTIONS]
        offset_options = await asyncio.gather(*offset_tasks)
        print(offset_options)
        self.write(json.dumps(offset_options))


class OffsetOffsetHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)

        price_per_unit = (await async_fetch('/product/get/' + str(request_data['vendor_id']) + '/' +
                                            str(OFFSET_PRODUCT_ID), GET))['carbon_cost']

        transaction_data = await async_fetch('/purchase/add', POST, data={
            'buyr_id': request_data['user_id'],
            'selr_id': request_data['vendor_id'],
            'price': request_data['offset_amount'] * price_per_unit,
            'carbon_cost': -1 * request_data['offset_amount'],
            'item_list': None
        })

        if transaction_data['status'] != 'success':
            self.write(json.dumps({'transaction_id': 0}))
        else:
            response_data = await async_fetch('/purchase/get/' + str(transaction_data['data']['prch_id']), GET)
            data = {
                'transaction_id': response_data['id'],
                'price': response_data['price'],
                'carbon_cost_offset': response_data['carbon_cost'],
                'vendor': response_data['selr_id'],
                'timestamp': response_data['ts']
            }
            self.write(json.dumps(data))

            response_data_1 = await async_fetch('/entity/get/' + str(request_data['user_id']), GET)
            response_data_1['carbon_offset'] += request_data['offset_amount']
            await async_fetch('/entity/update', POST, data=response_data_1)