from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler


class EcranHandler(BaseHTTPRequestHandler):
    pass


class EcranServer(HTTPServer):

    def __init__(self, address, canvas=None, **kw):
        HTTPServer.__init__(self, address, EcranHandler, **kw)
        self.canvas = canvas
        self._thread = Thread(target=self.serve_forever)

    def start(self):
        self._thread.start()


if __name__ == "__main__":
    server = EcranServer(('', 5566))
    server.start()
    sa = server.socket.getsockname()
    print('Listening on {} port {} ...'.format(*sa))
    try:
        from time import sleep
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        server.shutdown()
        print('\nKeyboard interrupt received, exiting.')
