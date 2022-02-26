import json
import tornado.web
from handlers.async_fetch import async_fetch, GET, POST

offset_data = [
            {
                'vendor_id': 13,
                'vendor': 'Generic Offset',
                'description': 'A blend of offsetting projects',
                # price in cents, as all prices
                'price': 100
            },
            {
                'vendor_id': 14,
                'vendor': 'Kiwi Carbon Capture Scheme',
                'description': 'Store carbon underground for thousands of years',
                'price': 314
            },
            {
                'vendor_id': 15,
                'vendor': 'Kakapo Tree Planting',
                'description': 'Rebuild the natural habitats',
                'price': 159
            },
            {
                'vendor_id': 16,
                'vendor': 'Kea Green Energy',
                'description': 'Renewable energy for all',
                'price': 265
            },
            {
                'vendor_id': 17,
                'vendor': 'Takahe Methane Combustion',
                'description': 'Reduce global warming by burning methane',
                'price': 358
            }
        ]

class OffsetGetHandler(tornado.web.RequestHandler):
    async def get(self):
        # TODO: incorporate offsetting info into separate database
        self.write(json.dumps(offset_data))

class OffsetOffsetHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)

        transaction_data = await async_fetch('/purchase/add', POST, data={
            'buyr_id': request_data['user_id'],
            'selr_id': request_data['vendor_id'],
            'price': request_data['carbon_cost_offset'] * next(offset['price'] for offset in offset_data
                                                               if offset['vendor_id'] == request_data['vendor_id']),
            'carbon_cost': -1 * request_data['carbon_cost_offset'],
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
            response_data_1['carbon_offset'] += request_data['carbon_cost_offset']
            await async_fetch('/entity/update', POST, data=response_data_1)