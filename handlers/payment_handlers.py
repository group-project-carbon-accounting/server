import tornado.web
from async_fetch import async_fetch, GET, POST

class PaymentProcessHandler(tornado.web.RequestHandler):
    async def post(self):
        pass

'''
class TransactionAddHandler(tornado.web.RequestHandler) :
    async def post(self):
        request_data = json.loads(self.request.body)




        response_data = await async_fetch('/purchase/add', POST, self.request.body)
        carbon = 0
        offset = 0
        if response_data['item_list'] and not data['carbon_cost'] :
            for key in data['item_list'] :
                response1 = await httpclient.AsyncHTTPClient().fetch("http://localhost:8889/product/get/" + str(key['comp_id']) + "/" + str(key['prod_id']), method = 'GET')
                details = json.loads(response1.body)
                carbon += details['carbon_cost']
        elif (data['carbon_cost']):
            if (data['carbon_cost'] >= 0) :
                carbon += data['carbon_cost']
            else :
                offset += data['carbon_cost']
        entityResponse = await httpclient.AsyncHTTPClient().fetch("http://localhost:8889/entity/get/" + str(data['buyr_id']), method = 'GET')
        entityDetails = json.loads(entityResponse.body)
        entityDetails['carbon_cost'] += carbon
        entityDetails['carbon_offset'] += offset
        newEntityResponse = await httpclient.AsyncHTTPClient().fetch("http://localhost:8888/entity/update", method = 'POST', body = json.dumps(entityDetails))
        self.write(response.body)
'''