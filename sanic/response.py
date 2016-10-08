import ujson
import httptools
from ujson import loads as json_loads
from urllib.parse import parse_qs

STATUS_CODES = {
    200: 'OK',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    400: 'Method Not Allowed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}

class HTTPResponse:
    __slots__ = ('body', 'status', 'content_type')

    def __init__(self, body=None, status=200, content_type='text/plain', body_bytes=b''):
        self.content_type = content_type

        if not body is None:
            self.body = body.encode('utf-8')
        else:
            self.body = body_bytes

        self.status = status

    def output(self, version="1.1", keep_alive=False):
        # This is all returned in a kind-of funky way
        # We tried to make this as fast as possible in pure python
        return b''.join([
            'HTTP/{} {} {}\r\n'.format(version, self.status, STATUS_CODES.get(self.status, 'FAIL')).encode(),
            b'Content-Type: ', self.content_type.encode(), b'\r\n',
            b'Content-Length: ', str(len(self.body)).encode(), b'\r\n',
            b'Connection: ', ('keep-alive' if keep_alive else 'close').encode(), b'\r\n',
            b'\r\n',
            self.body,
        ])

def json(body, status=200):
    return HTTPResponse(ujson.dumps(body), status=status, content_type="application/json")
def text(body, status=200):
    return HTTPResponse(body, status=status, content_type="text/plain")
def html(body, status=200):
    return HTTPResponse(body, status=status, content_type="text/html")