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
        self.read_request_body()
        self.send_response(200)
        if self.server.paypal_mode == 'valid':
            self.wfile.write("\nVERIFIED")
        else:
            self.wfile.write("\nINVALID")

    def log_message(self, format, *args):
        # avoid log output to stderr
        pass

    def read_request_body(self):
        """Read request body and store it at server.
        """
        length = int(self.headers.get('Content-Length', 0))
        posted_body = None
        if length:
            posted_body = self.rfile.read(length)
        self.server.last_request_body = posted_body


@contextmanager
def http_server(handler_cls=None, do_ssl=False, paypal_mode='valid'):
    # the idea for this context manager comes from
    #
    # http://theyougen.blogspot.de/2012/10/
    #        my-best-python-http-test-server-so-far.html
    #
    if handler_cls is None:
        handler_cls = Handler
    httpd = TCPServer(("", 0), handler_cls)
    httpd.paypal_mode = paypal_mode
    httpd.last_request_body = None
    proto = "http"
    if do_ssl:
        proto = "https"
        httpd.socket = ssl.wrap_socket(
            httpd.socket, certfile=CERTFILE, server_side=True,
            ssl_version=ssl.PROTOCOL_SSLv23)
    t = threading.Thread(target=httpd.serve_forever)
    t.setDaemon(True)
    t.start()
    port = httpd.server_address[1]
    httpd.url = '%s://localhost:%s' % (proto, port)
    try:
        yield httpd
    finally:
        httpd.shutdown()
