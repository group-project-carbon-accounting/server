import tornado.web
from async_fetch import async_fetch, GET, POST

class ProductAddHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await async_fetch('/product/add', method=POST, data=self.request.body)
        self.write(response.body)

class ProductUpdateHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await async_fetch('/product/update', method=POST, data=self.request.body)
        self.write(response.body)

class ProductGetHandler(tornado.web.RequestHandler):
    async def get(self, comp_id, prod_id):
        response = await async_fetch('/product/get/' + comp_id + '/' + prod_id, method=GET)
        self.write(response.body)
