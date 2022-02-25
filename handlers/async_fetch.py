import json
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

URL = 'http://127.0.0.1:8888'
POST = 'POST'
GET = 'GET'

async def async_fetch(url_suffix, method, data=None):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(HTTPRequest(url=URL + url_suffix, method=method,
                                                   body=json.dumps(data) if data is not None else None))
    return json.loads(response.body)