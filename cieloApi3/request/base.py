import uuid

from future.utils import raise_with_traceback
from requests import Request, Session

from .exceptions import CieloRequestException


class Base(object):
    def __init__(self, merchant):

        self.merchant = merchant

    def send_request(self, method, uri, data=None, params=None):

        s = Session()

        body = data

        headers = {
            'User-Agent': "CieloEcommerce/3.0 Python SDK",
            'RequestId': str(uuid.uuid4()),
            'MerchantId': self.merchant.id,
            'MerchantKey': self.merchant.key
        }

        if not body:
            headers['Content-Length'] = '0'
        else:
            headers["Content-Type"] = "application/json"

            if not isinstance(data, dict):
                body = body.toJSON()

        req = Request(method, uri, data=body, headers=headers, params=params)

        prep = s.prepare_request(req)

        response = s.send(prep)

        if 'json' in response.headers.get('content-type', '').lower():
            answers = response.json()
        else:
            answers = [{
                'Code': str(response.status_code),
                'Message': response.text
            }]

        if response.status_code >= 400:
            raise_with_traceback(CieloRequestException(response=response,
                                                       **answers[0]))

        return answers
