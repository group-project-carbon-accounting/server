import tornado.web
from handlers.async_fetch import async_fetch, GET, POST
import json
from tornado import httpclient

class PaymentProcessHandler(tornado.web.RequestHandler):
    async def post(self):
        request_data = json.loads(self.request.body)
        response_data = await async_fetch('/purchase/add', POST, request_data)
        carbon = 0
        offset = 0
        if (request_data['item_list'] and request_data['carbon_cost'] == 0) :
            for key in request_data['item_list'] :
                product_response = await async_fetch("/product/get/" + str(key['comp_id']) + "/" + str(key['prod_id']), GET)
                carbon += product_response['carbon_cost']
        else:
            if (request_data['carbon_cost'] >= 0) :
                carbon += request_data['carbon_cost']
            else :
                offset += request_data['carbon_cost']
        
        entityResponse = await async_fetch("/entity/get/" + str(request_data['buyr_id']), method = 'GET')
        entityResponse['carbon_cost'] += carbon
        entityResponse['carbon_offset'] += offset
        newEntityResponse = await async_fetch("/entity/update", POST, entityResponse)
        request_data['carbon_cost'] = carbon
        update_response = await async_fetch('/purchase/update', POST, request_data)
        self.write(json.dumps(update_response))
