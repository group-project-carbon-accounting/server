import tornado.web
from async_fetch import async_fetch, GET, POST

class EntityGetHandler(tornado.web.RequestHandler) :
    async def get(self, user_id):
        response = await async_fetch('/entity/get/' + user_id, method=GET)
        self.write(response.body)