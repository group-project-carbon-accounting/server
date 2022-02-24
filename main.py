from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado_sqlalchemy import SQLAlchemy
from tornado import httpclient
import tornado
import json
from handlers.product_handlers import AddProductHandler, UpdateProductHandler, GetProductHandler
from handlers.entity_handlers import GetEntityHandler
from handlers.transaction_handlers import TransactionGetRecentHandler

class MainHandler(tornado.web.RequestHandler) :
    def post(self):
        data = json.loads(self.request.body)
        self.write(str(data['test']))

class AddTransactionHandler(tornado.web.RequestHandler) :
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/purchase/add", method = 'POST', body = self.request.body)
        data = json.loads(self.request.body)
        carbon = 0
        offset = 0
        if (data['item_list'] and not data['carbon_cost']) :
            for key in data['item_list'] :
                response1 = await httpclient.AsyncHTTPClient().fetch("http://localhost:8889/product/get/" + str(key['comp_id']) + "/" + str(key['prod_id']), method = 'GET')
                details = json.loads(response1.body)
                carbon += details['carbon_cost']
        elif (data['carbon_cost']):
            if (data['carbon_cost'] >= 0) :
                carbon += data['carbon_cost']
            else :
                offset += data['carbon_cost']
        entityResponse = await httpclient.AsyncHTTPClient().fetch("http://localhost:8889/entity/get/" + str(data['buyr_id']), method = 'GET')
        entityDetails = json.loads(entityResponse.body)
        entityDetails['carbon_cost'] += carbon
        entityDetails['carbon_offset'] += offset
        newEntityResponse = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/entity/update", method = 'POST', body = json.dumps(entityDetails))
        self.write(response.body)

class GetTransactionHandler(tornado.web.RequestHandler):
    async def get(self, prch_id):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/purchase/get/" + str(prch_id), method = 'GET')
        self.write(response.body)

class UpdateTransactionHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/purchase/update", method = 'POST', body = self.request.body)
        self.write(response.body)


app = Application ([
    (r'/test', MainHandler),  
    (r'/transaction/add', AddTransactionHandler),
    (r'/transaction/get/(?P<prch_id>[0-9]*)', GetTransactionHandler),
    (r'/transaction/get_recent/(?P<user_id>[0-9]*)/(?P<num_of_days>[0-9]*)', TransactionGetRecentHandler),
    (r'/transaction/update', UpdateTransactionHandler), 
    (r'/product/add', AddProductHandler), 
    (r'/product/update', UpdateProductHandler), 
    (r'/product/get/(?P<comp_id>[0-9]*)/(?P<prod_id>[0-9]*)', GetProductHandler),
    (r'/entity/get/(?P<user_id>[0-9]*)', GetEntityHandler)
])

if __name__ == '__main__':
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
