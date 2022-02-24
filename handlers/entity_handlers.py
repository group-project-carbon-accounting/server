import tornado
from tornado import httpclient

class GetEntityHandler(tornado.web.RequestHandler) :
    async def get(self, user_id):
        response = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/entity/get/" + str(user_id) , method = 'GET')
        self.write(response.body)