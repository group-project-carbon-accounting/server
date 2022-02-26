import asyncio
import tornado.web
import json
from handlers.async_fetch import async_fetch, GET, POST, async_get_product_data


class PaymentProcessHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)

        carbon_cost = [0]
        if 'products' in request_data:
            product_tasks = [async_get_product_data(product, carbon_cost) for product in request_data['products']]
            try:
                await asyncio.gather(product_tasks)
            except Exception:
                self.write(json.dumps({'success': False}))
                return
        elif 'carbon_cost' in request_data:
            carbon_cost[0] = request_data['carbon_cost']

        transaction_data = await async_fetch('/purchase/add', POST, data={
            'buyr_id': request_data['user_id'],
            'selr_id': request_data['vendor_id'],
            'price': request_data['amount'],
            'carbon_cost': carbon_cost[0],
            'item_list': [{'prod_id': product['product_id'], 'comp_id': product['company_id']}
                          for product in request_data['products']] if 'products' in request_data else None
        })

        self.write(json.dumps({'success': (transaction_data['status'] == 'success')}))

        response_data_1 = await async_fetch('/entity/get/' + str(request_data['user_id']), GET)
        response_data_1['carbon_cost'] += carbon_cost[0]
        await async_fetch('/entity/update', POST, data=response_data_1)