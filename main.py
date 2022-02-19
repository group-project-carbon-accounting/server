from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado_sqlalchemy import SQLAlchemy
from tornado import httpclient
import tornado
import json
import urllib
import process_payment
import general.account
import general.user

class AddTransactionHandler(tornado.web.RequestHandler) :
    def get(self):
        transaction = process_payment(self.request.body)
        self.write(transaction)

class CreateUserHandler(tornado.web.RequestHandler) :
    def get(self):
        data = json.loads(self.request.body)
        general.user(self, data['username'], data['email'])

class CreateAccountHandler(tornado.web.RequestHandler) :
    def get(self):
        data = json.loads(self.request.body)
        general.account(self, data['user'], data['account_type'])



db = SQLAlchemy("postgresql://postgres:postgres@localhost:5432/db")


app = Application ([
    #(r'/test', MainHandler), 
    (r'/user/create', CreateUserHandler), 
    (r'/account/create', CreateAccountHandler), 
    (r'/transaction/add', AddTransactionHandler),
    # (r'/transaction/update', UpdateTransactionHAndler)
])

if __name__ == '__main__':
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()