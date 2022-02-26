import tornado.web
import json
from handlers.async_fetch import async_fetch, GET, POST

class ProductAddHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)
        data = {
            'prod_id': request_data['product_id'],
            'comp_id': request_data['company_id'],
            'carbon_cost': request_data['carbon_cost_offset']
        }
        response = await async_fetch('/product/add', method=POST, data=data)
        self.write(json.dumps({'success': (response['status'] == 'success')}))


class ProductUpdateHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)
        data = {
            'prod_id': request_data['product_id'],
            'comp_id': request_data['company_id'],
            'carbon_cost': request_data['carbon_cost_offset']
        }
        response = await async_fetch('/product/update', method=POST, data=data)
        self.write(json.dumps({'success': (response['status'] == 'success')}))

class ProductGetHandler(tornado.web.RequestHandler):
    async def get(self, company_id, product_id):
        response_data = await async_fetch('/product/get/' + company_id + '/' + product_id, method=GET)
        self.write(json.dumps({'generic': (response_data['comp_id'] is None),
                               'carbon_cost_offset': response_data['carbon_cost']}))
