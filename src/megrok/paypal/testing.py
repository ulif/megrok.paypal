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


class StoppableHTTPServer(TCPServer):
    """An HTTP server for testing.

    This server, when `start()`ed, runs `serve_forever` in a separate
    thread, so we can `shutdown()` it at any time.

    This server accepts no port or IP to bind to. Instead it binds to
    localhost and binds to some arbitrary unused port. Use `url()` to
    get the URL of the server, including port. `server_address` will
    give that information as well.

    If `do_ssl` is True, we use the locally stored certificate for SSL
    communication.

    This server handles requests via a `Handler` instance, which
    normally stores request bodies and content types in attributes
    `last_request_body`, `last_request_content_type`. See tests for
    samples.
    """
    url = None
    do_ssl = False

    def __init__(self, do_ssl=False, paypal_mode='valid'):
        TCPServer.__init__(self, ("", 0), Handler)  # old-style base?
        self.do_ssl = do_ssl
        self.paypal_mode = paypal_mode
        self.last_request_body = None
        self.last_request_content_type = None

    def start(self):
        """Start server in separate thread.
        """
        proto = "http"
        if self.do_ssl:
            proto = "https"
            self.socket = ssl.wrap_socket(
                self.socket, certfile=CERTFILE, server_side=True,
                ssl_version=ssl.PROTOCOL_SSLv23)
        t = threading.Thread(target=self.serve_forever)
        t.setDaemon(True)
        t.start()
        port = self.server_address[1]
        self.url = '%s://localhost:%s' % (proto, port)

    def shutdown(self):
        return TCPServer.shutdown(self)


@contextmanager
def http_server(do_ssl=False, paypal_mode='valid'):
    server = StoppableHTTPServer(do_ssl=do_ssl, paypal_mode=paypal_mode)
    server.start()
    try:
        yield server
    finally:
        server.shutdown()


class HTTPServerLayer(object):
    """A test layer, usable by `zope.testrunner`.

    Use it as a layer in a test case. Provides `server` attribute, an
    instance if a running `StoppableHTTPServer`.
    """
    @classmethod
    def setUp(cls):
        cls.server = StoppableHTTPServer()
        cls.server.start()

    @classmethod
    def tearDown(cls):
        cls.server.shutdown()
