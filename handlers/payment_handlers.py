import tornado.web
from async_fetch import async_fetch, GET, POST

class PaymentProcessHandler(tornado.web.RequestHandler):
    async def post(self):
        pass