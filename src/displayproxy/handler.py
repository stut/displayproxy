"""displayproxy server module."""
from http.server import BaseHTTPRequestHandler, HTTPStatus
import io
import json
from PIL import Image


def MakeProxyHandler(display):
    class ProxyHandler(BaseHTTPRequestHandler):
        """
        HTTP request handler for the ProxyServer.
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == '/info':
                self._do_get_info()
            else:
                self._do_404()

        def do_POST(self):
            if self.path == '/update':
                self._do_post_update()
            elif self.path == '/shutdown':
                self._do_shutdown()
            else:
                self._do_404()

        def _do_404(self):
            """Send a 404 response."""
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes('Not found', 'utf8'))

        def _do_get_info(self):
            """Return information about the display."""
            info = {
                'width': display.width,
                'height': display.height,
            }
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(info), 'utf8'))

        def _do_post_update(self):
            """Update the display with the posted image."""
            content_len = int(self.headers.get('content-length', 0))
            if content_len == 0:
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.end_headers()
                self.wfile.write(bytes('No content length', 'utf8'))
                return

            post_body = self.rfile.read(content_len)
            bytes_io = io.BytesIO(post_body)
            img = Image.open(bytes_io)

            display.update(img)

            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()

        def _do_shutdown(self):
            """Stop the display which will cause the process to end."""
            display.shutdown()
            self.send_response(HTTPStatus.ACCEPTED)
            self.end_headers()

    return ProxyHandler
