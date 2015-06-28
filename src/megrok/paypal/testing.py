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
        self.send_response(200)
        if self.server.paypal_mode == 'valid':
            self.wfile.write("\nVERIFIED")
        else:
            self.wfile.write("\nINVALID")

    def log_message(self, format, *args):
        # avoid log output to stderr
        pass


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
    try:
        yield '%s://localhost:%s' % (proto, port)
    finally:
        httpd.shutdown()
