# Support for testing.
import os
import ssl
import threading
from contextlib import contextmanager
try:                        # Python 3.x
    from socketserver import TCPServer
except ImportError:         # Python 2.x
    from SocketServer import TCPServer
try:                        # Python 3.x
    from http.server import BaseHTTPRequestHandler
except ImportError:         # Python 2.x
    from BaseHTTPServer import BaseHTTPRequestHandler


CERTFILE = os.path.join(
    os.path.dirname(__file__), 'tests', 'fakeserver_ssl.pem')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.wfile.write("\nOk")

    def do_POST(self):
        self.read_request_data()
        self.send_response(200)
        if self.server.paypal_mode == 'valid':
            self.wfile.write("\nVERIFIED")
        else:
            self.wfile.write("\nINVALID")

    def log_message(self, format, *args):
        # avoid log output to stderr
        pass

    def read_request_data(self):
        """Read request data (body, content-type) and store it at server.
        """
        self.server.last_request_content_type = self.headers.get(
            'Content-Type', None)
        length = int(self.headers.get('Content-Length', 0))
        posted_body = None
        if length:
            posted_body = self.rfile.read(length)
        self.server.last_request_body = posted_body


class StoppableHTTPServer(object):

    url = None
    server = None
    do_ssl = False

    @property
    def last_request_body(self):
        return self.server.last_request_body

    @property
    def last_request_content_type(self):
        return self.server.last_request_content_type

    def __init__(self, do_ssl=False, paypal_mode='valid'):
        self.do_ssl = do_ssl
        self.server = TCPServer(("", 0), Handler)
        self.server.paypal_mode = paypal_mode
        self.server.last_request_body = None
        self.server.last_request_content_type = None

    def start(self):
        proto = "http"
        if self.do_ssl:
            proto = "https"
            self.server.socket = ssl.wrap_socket(
                self.server.socket, certfile=CERTFILE, server_side=True,
                ssl_version=ssl.PROTOCOL_SSLv23)
        t = threading.Thread(target=self.server.serve_forever)
        t.setDaemon(True)
        t.start()
        port = self.server.server_address[1]
        self.url = '%s://localhost:%s' % (proto, port)

    def shutdown(self):
        self.server.shutdown()


@contextmanager
def http_server(do_ssl=False, paypal_mode='valid'):
    server = StoppableHTTPServer(do_ssl=do_ssl, paypal_mode=paypal_mode)
    server.start()
    try:
        yield server
    finally:
        server.shutdown()
