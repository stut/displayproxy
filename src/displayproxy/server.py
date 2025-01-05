"""displayproxy server module."""

import atexit
from http.server import HTTPServer
from threading import Thread

from handler import MakeProxyHandler

__all__ = ['ProxyServer']


class ProxyServer:
    """
    ProxyServer is an HTTP server that can display images on an Inky display
    or using pygame.
    """

    def __init__(self, display_type: str,
                 host: str = 'localhost', port: int = 8000,
                 buttons: str = '', options: str = ''):
        """
        Create an ProxyServer.

        :param host: The host to bind the server to.
        :param port: The port to bind the server to.
        :param buttons: A string of button configuration in the format
            'pin=label,pin=label,...'.
        :param options: A display type specific string of options in the
            format 'key=value,key=value,...'.
        """
        self._host = host
        self._port = port

        if display_type == 'inky':
            from display_inky import InkyDisplay
            self._display = InkyDisplay(buttons, options)
        elif display_type == 'pygame':
            from display_pygame import PygameDisplay
            self._display = PygameDisplay(buttons, options)
        else:
            exit(f"Unsupported display type: {display_type}; supported: inky, pygame")

        atexit.register(self._display.cleanup)

    def start(self):
        """Start the server and run the display."""
        server_address = (self._host, self._port)
        httpd = HTTPServer(server_address, MakeProxyHandler(self._display))
        t = Thread(target=httpd.serve_forever)
        t.start()
        self._display.run()
        httpd.shutdown()
        t.join()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost', type=str, metavar='HOST',
                        help='host to listen on (default: %(default)s)')
    parser.add_argument('--port', default=8000, type=int, metavar='PORT',
                        help='port to listen on (default: %(default)s)')
    parser.add_argument('--buttons', default='', type=str, metavar='BUTTONS',
                        help='button configuration (see docs; default: "")')
    parser.add_argument('--options', default='', type=str, metavar='OPTIONS',
                        help='type-specific display options (see docs; default: "")')
    parser.add_argument('display_type', type=str, metavar='DISPLAY_TYPE',
                        nargs='?', default='pygame',
                        help='type of display to use (supported: inky, pygame; default: pygame)')
    args = parser.parse_args()

    try:
        ProxyServer(
            args.display_type,
            host=args.host,
            port=args.port,
            buttons=args.buttons,
            options=args.options,
        ).start()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
