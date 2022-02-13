from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado_sqlalchemy import SQLAlchemy
from tornado import httpclient
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

db = SQLAlchemy("postgresql://postgres:postgres@localhost:5432/db")


app = Application ([
    (r'/test', MainHandler), 
    (r'/user/create', CreateUserHandler), 
    (r'/account/create', CreateAccountHandler), 
    (r'/transaction/add', AddTransactionHandler),
    (r'/transaction/update', UpdateTransactionHAndler)
])

if __name__ == '__main__':
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()