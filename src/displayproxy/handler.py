"""displayproxy server module."""
from http.server import BaseHTTPRequestHandler, HTTPStatus
import io
import json
from PIL import Image

from displayproxy.__version__ import __version__


def MakeProxyHandler(display):
    class ProxyHandler(BaseHTTPRequestHandler):
        """
        HTTP request handler for the ProxyServer.
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def _send_headers(self, status: HTTPStatus, headers: dict = {}):
            """Set the response headers."""
            self.send_response(status)
            self.send_header('Server', f'displayproxy/{__version__} (https://github.com/stut/displayproxy)')
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()

        def do_GET(self):
            if self.path == '/info':
                self._do_get_info()
            elif self.path == '/buttons':
                self._do_get_buttons()
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
            self._send_headers(HTTPStatus.NOT_FOUND, {'Content-type': 'text/plain'})
            self.wfile.write(bytes('Not found', 'utf8'))

        def _do_get_info(self):
            """Return information about the display."""
            info = {
                'width': display.width,
                'height': display.height,
            }
            self._send_headers(HTTPStatus.OK, {'Content-type': 'application/json'})
            self.wfile.write(bytes(json.dumps(info), 'utf8'))

        def _do_get_buttons(self):
            """Return the current state of the buttons."""
            self._send_headers(HTTPStatus.OK, {'Content-type': 'application/json'})
            self.wfile.write(bytes(json.dumps(display.get_button_status()), 'utf8'))

        def _do_post_update(self):
            """Update the display with the posted image."""
            content_len = int(self.headers.get('content-length', 0))
            if content_len == 0:
                self._send_headers(HTTPStatus.BAD_REQUEST)
                self.wfile.write(bytes('No content length', 'utf8'))
                return
            if content_len > display.max_upload_size:
                self._send_headers(HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
                self.wfile.write(bytes('Content too large', 'utf8'))
                return

            post_body = self.rfile.read(content_len)
            bytes_io = io.BytesIO(post_body)
            img = Image.open(bytes_io)
            display.update(img)

            self._send_headers(HTTPStatus.NO_CONTENT)

        def _do_shutdown(self):
            """Stop the display which will cause the process to end."""
            display.shutdown()
            self._send_headers(HTTPStatus.ACCEPTED)

    return ProxyHandler
