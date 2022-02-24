import tornado
from tornado import httpclient

class AddProductHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/add", method = 'POST', body = self.request.body)
        self.write(response.body)

class UpdateProductHandler(tornado.web.RequestHandler):
    async def post(self):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/update", method = 'POST', body = self.request.body)
        self.write(response.body)

class GetProductHandler(tornado.web.RequestHandler):
    async def get(self, comp_id, prod_id):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/product/get/" + str(comp_id) +"/" + str(prod_id), method = 'GET')
        self.write(response.body)
