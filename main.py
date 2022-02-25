from tornado.ioloop import IOLoop
from handlers import entity_handlers, offset_handlers, payment_handlers, product_handlers, transaction_handlers
import tornado.web
import json


class TestHandler(tornado.web.RequestHandler):
    # post test
    def post(self):
        data = json.loads(self.request.body)
        self.write(str(data['test']))

    # get test
    def get(self, test):
        self.write(test)

# TODO: implement these handlers
'''
(r'/product/add', AddProductHandler), 
(r'/product/update', UpdateProductHandler), 
(r'/product/get/(?P<comp_id>[0-9]*)/(?P<prod_id>[0-9]*)', GetProductHandler),
(r'/entity/get/(?P<user_id>[0-9]*)', GetEntityHandler)
'''

if __name__ == '__main__':
    app = tornado.web.Application([
        ('/test', TestHandler),
        ('/test/(?P<test>.*)', TestHandler),
        ('/transaction/get/(?P<transaction_id>[0-9]+)', transaction_handlers.TransactionGetHandler),
        ('/transaction/get_recent/(?P<user_id>[0-9]+)/(?P<num_of_days>[0-9]+)',
         transaction_handlers.TransactionGetRecentHandler),
        ('/transaction/update', transaction_handlers.TransactionUpdateHandler),
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
