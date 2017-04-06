import json


class CieloRequestException(Exception):
    Code = None
    Message = None
    request = None
    response = None

    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None and not self.request and
                hasattr(response, 'request')):
            self.request = self.response.request
        self.Code = int(kwargs.pop('Code', None))
        self.Message = kwargs.pop('Message', None)

    def __str__(self):
        data_send = json.loads(self.request.body or 'null')

        errors = []
        errors.append('* [%s] %s\r\n' % (self.Code, self.Message))
        errors.append('Method: %s\r\n' % self.request.method)
        errors.append('Uri: %s\r\n' % self.response.url)
        errors.append('Data: %s\r\n' % json.dumps(data_send, indent=2))
        return ''.join(errors)
