import json
import time
import tornado
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

URL = 'http://127.0.0.1:8888'
POST = 'POST'
GET = 'GET'

async def async_fetch(url_suffix, method, data=None):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + url_suffix, method=method,
                                                   body=json.dumps(data) if data is not None else None))
    return json.loads(response.body)


class TransactionGetRecentHandler(RequestHandler):
    async def get(self, user_id, num_of_days):

        # add 60 seconds just in case of high latency
        ts_now = int(time.time()) + 60
        ts_past = ts_now - int(num_of_days) * 86400 if int(num_of_days) != 0 else 0
        response_data = await async_fetch('/entity/get/' + user_id + '?start_ts=' + str(ts_now) +
                                          '&end_ts=' + str(ts_past), GET)
        print(json.dumps(response_data))



# TODO: move this to separate test module
app = Application([
        ('/transaction/get_recent/(?P<user_id>[0-9]+)/(?P<num_of_days>[0-9]+)', TransactionGetRecentHandler)
    ])

if __name__ == '__main__':
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()