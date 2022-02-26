from handlers import user_handlers, offset_handlers, payment_handlers, product_handlers, transaction_handlers
import tornado.web, tornado.ioloop
import json


class TestHandler(tornado.web.RequestHandler):
    # post test
    def post(self):
        data = json.loads(self.request.body)
        self.write(str(data['test']))

    # get test
    def get(self, test):
        self.write(test)


if __name__ == '__main__':
    app = tornado.web.Application([
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
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()

'''
For testing purposes:

e.g. 
GET     curl http://localhost:8889/test/12
POST    curl -X POST http://localhost:8889/test -H "Content-Type: application/json" -d '{"test": 12}'

In both cases, it should write 12
'''
