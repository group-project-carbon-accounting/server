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

async def async_get_product_data(product, carbon_cost_sum):
    product_data = await async_fetch('/product/get/' + str(product['company_id']) + '/' + str(product['product_id']), GET)
    if product_data['carbon_cost'] < 0:
        raise Exception
    carbon_cost_sum[0] += product_data['carbon_cost']
    return product_data