import unittest
import json
import tornado.testing
import tornado.web
import main
from .. import handlers
from handlers import user_handlers, offset_handlers, payment_handlers, product_handlers, transaction_handlers
from server.main import TestHandler, user_handlers, offset_handlers, payment_handlers, product_handlers, transaction_handlers


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

    def test_addProduct(self):
        response = self.fetch('/product/add', method='POST', body='''{
    "prod_id": 2,
    "comp_id": 6,
    "carbon_cost": 1000
}''')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), json.loads('''{"success": "true"}'''))
    

    
    
unittest.main()