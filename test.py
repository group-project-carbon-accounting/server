import unittest
import json
import tornado.testing
import tornado.web
from handlers import user_handlers, offset_handlers, payment_handlers, product_handlers, transaction_handlers
from main import TestHandler

class Test(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
        ('/test', TestHandler),
        ('/test/(?P<test>.*)', TestHandler),
        # App endpoints
        ('/user/get/(?P<user_id>[0-9]+)', user_handlers.UserGetHandler),
        ('/transaction/get/(?P<transaction_id>[0-9]+)', transaction_handlers.TransactionGetHandler),
        ('/transaction/get_recent/(?P<user_id>[0-9]+)/(?P<num_of_days>[0-9]+)',
         transaction_handlers.TransactionGetRecentHandler),
        ('/transaction/update', transaction_handlers.TransactionUpdateHandler),
        ('/transaction/update_products', transaction_handlers.TransactionUpdateProductsHandler),
        ('/offset/get', offset_handlers.OffsetGetHandler),
        ('/offset/offset', offset_handlers.OffsetOffsetHandler),
        # Company endpoints
        ('/product/add', product_handlers.ProductAddHandler),
        ('/product/update', product_handlers.ProductUpdateHandler),
        ('/product/get/(?P<company_id>[0-9]+)/(?P<product_id>[0-9]+)', product_handlers.ProductGetHandler),
        # Payment endpoints
        ('/payment', payment_handlers.PaymentProcessHandler)
    ])

    def test_get(self):
        response = self.fetch('/test/hello', method = 'GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode("utf-8"), "hello")

    def test_post(self):
        response = self.fetch('/test', method = 'POST', body = '''{
            "test": "hello world"
        }''')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode("utf-8"), "hello world")

    def test_addProduct(self):
        response = self.fetch('/product/add', method='POST', body='''{
            "product_id": 1,
            "company_id": 7,
            "carbon_cost_offset": 1000
        }''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"success": true}'''))

    def test_getProduct(self):
        response = self.fetch('/product/get/7/1', method = 'GET')
        self.assertEqual(response.code, 200)
    
    def test_updateProduct(self):
        response = self.fetch('/product/update', method = 'POST', body = '''{
            "product_id": 1, 
            "company_id": 7, 
            "carbon_cost_offset": 2000
        }''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"success": true}'''))
        response = self.fetch('/product/get/7/1', method = 'GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"generic": false, "carbon_cost_offset": 2000}'''))

    def test_getUser(self):
        response = self.fetch('/user/get/7', method = 'GET')
        self.assertEqual(response.code, 200)  

    def test_payment_with_items(self):
        response = self.fetch('/payment', method = 'POST', body = '''{
            "user_id":5,
            "vendor_id":3,
            "amount":500, 
            "item_list": [{"product_id":1,"company_id":7}]
        }''')  
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"success": true}'''))
    
    def test_transaction_get(self):
        response = self.fetch('/transaction/get/7', method = 'GET')
        self.assertEqual(response.code, 200)

    def test_transaction_update(self):
        response = self.fetch('/transaction/update', method = 'POST', body = '''{
            "transaction_id": 1,
            "carbon_cost_offset": 100
            }''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"success": true}'''))
    
    def test_transaction_updateProducts(self):
        response = self.fetch('/transaction/update_products', method = 'POST', body = '''{
            "transaction_id": 1,
	        "products":
	        [{
			    "company_id": 7,
			    "product_id": 1
		    }]
        }''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"success": true}'''))   
    
unittest.main()