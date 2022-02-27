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

async def async_get_offset_options(offset_company_id, offset_description, offset_product_id):
    product_data = await async_fetch('/product/get/' + str(offset_company_id) + '/' + str(offset_product_id), GET)
    company_data = await async_fetch('/entity/get/' + str(offset_company_id), GET)
    return {
        'vendor_id': offset_company_id,
        'vendor': company_data['display_name'],
        'description': offset_description,
        'price': product_data['carbon_cost']
    }

async def async_get_product_info(ids, products):
    product_data = await async_fetch('/product/get/' + str(ids['prod_id']), GET)
    company_data = await async_fetch('/entity/get/' + str(ids['comp_id']), GET)
    products.append({'company_name': company_data['display_name'], 'product_name': product_data['item_name']})