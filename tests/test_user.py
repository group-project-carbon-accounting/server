import unittest
import json
import tornado.testing
import tornado.web
import sys
sys.path.insert(0, '/Users/riya/Documents/Part 1B/Group Project/server')
from handlers.entity_handlers import GetEntityHandler
from handlers.product_handlers import AddProductHandler, GetProductHandler, UpdateProductHandler
from main import MainHandler, AddTransactionHandler, GetTransactionHandler, UpdateTransactionHandler
from handlers.transaction_handlers import TransactionGetRecentHandler

class Test(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
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

    def test_addProduct(self):
        response = self.fetch('/product/add', method='POST', body='''{
    "prod_id": 2,
    "comp_id": 6,
    "carbon_cost": 1000
}''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"status": "success"}'''))
    
    def test_getProduct(self):
        response = self.fetch('/product/get/6/2', method = 'GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{
    "prod_id": 2,
    "comp_id": 6,
    "carbon_cost": 1000
}'''))

    def test_updateProduct(self):
        response = self.fetch('/product/update', method = 'POST', body = '''{
    "prod_id": 2,
    "comp_id": 6,
    "carbon_cost": 2000
}''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"status": "success"}'''))
    
    
unittest.main()