from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado_sqlalchemy import SQLAlchemy
from tornado import httpclient
import tornado
import json
#import general.account
#import general.user

class MainHandler(tornado.web.RequestHandler) :
    def post(self):
        data = json.loads(self.request.body)
        self.write(str(data['test']))

async def calculateCarbonCost(x):
    x = json.loads(x)
    if (x['item_list']):
        for key in x['item_list'] :
            response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/get/" + str(key['comp_id']) + "/" + str(key['prod_id']), method = 'GET')
            return response.body['carbon_cost']


class AddTransactionHandler(tornado.web.RequestHandler) :
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/purchase/add", method = 'POST', body = self.request.body)
        data = json.loads(self.request.body)
        carbon = 0
        if (data['item_list']) :
            for key in data['item_list'] :
                response1 = await httpclient.AsyncHTTPClient().fetch("http://localhost:8889/product/get/" + str(key['comp_id']) + "/" + str(key['prod_id']), method = 'GET')
                details = json.loads(response1.body)
                carbon += details['carbon_cost']
        entityResponse = await httpclient.AsyncHTTPClient().fetch("http://localhost:8889/entity/get/" + str(data['buyr_id']), method = 'GET')
        entityDetails = json.loads(entityResponse.body)
        entityDetails['carbon_cost'] += carbon
        newEntityResponse = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/entity/update", method = 'POST', body = json.dumps(entityDetails))
        self.write(response.body)

class CreateUserHandler(tornado.web.RequestHandler) :
    def get(self):
        data = json.loads(self.request.body)
        #general.user(self, data['username'], data['email'])

class CreateAccountHandler(tornado.web.RequestHandler) :
    def get(self):
        data = json.loads(self.request.body)
        #general.account(self, data['user'], data['account_type'])

class GetTransactionHandler(tornado.web.RequestHandler):
    async def get(self, prch_id):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/purchase/get/" + str(prch_id), method = 'GET')
        self.write(response.body)

class UpdateTransactionHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/purchase/update", method = 'POST', body = self.request.body)
        self.write(response.body)

class AddProductHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/add", method = 'POST', body = self.request.body)
        self.write(response.body)

class UpdateProductHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/update", method = 'POST', body = self.request.body)
        self.write(response.body)

class GetEntityHandler(tornado.web.RequestHandler) :
    async def get(self, user_id):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/entity/get/" + str(user_id) , method = 'GET')
        self.write(response.body)

class GetRecentTransactionHandler(tornado.web.RequestHandler):
    async def get(self, user_id, x):
        self.write("Hello world")

class GetProductHandler(tornado.web.RequestHandler):
    async def get(self, comp_id, prod_id):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/get/" + str(comp_id) +"/" + str(prod_id), method = 'GET')
        self.write(response.body)

db = SQLAlchemy("postgresql://postgres:postgres@localhost:5432/db")


app = Application ([
    #(r'/test', MainHandler), 
    (r'/user/create', CreateUserHandler), 
    (r'/account/create', CreateAccountHandler), 
    (r'/transaction/add', AddTransactionHandler),
    (r'/transaction/get/(?P<prch_id>[0-9]*)', GetTransactionHandler),
    (r'/transaction/get_recent/(?P<user_id>[0-9]*)/(?P<x>[0-9]*)', GetRecentTransactionHandler),
    (r'/transaction/update', UpdateTransactionHandler), 
    (r'/product/add', AddProductHandler), 
    (r'/product/update', UpdateProductHandler), 
    (r'/product/get/(?P<comp_id>[0-9]*)/(?P<prod_id>[0-9]*)', GetProductHandler),
    (r'/entity/get/(?P<user_id>[0-9]*)', GetEntityHandler)
])

if __name__ == '__main__':
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
