import tornado.web
import json
from handlers.async_fetch import async_fetch, GET, POST

class UserGetHandler(tornado.web.RequestHandler) :
    async def get(self, user_id):
        response_data = await async_fetch('/entity/get/' + user_id, method=GET)
        response_data['name'] = response_data['display_name']
        del(response_data['id'])
        del(response_data['display_name'])
        self.write(json.dumps(response_data))