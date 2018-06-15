from threading import Event

from .canvas import Canvas
from .server import EcranServer
from .render import FlatRenderer


class Ecran:
    """Ecran server and renderer"""

    def __init__(self, size=(256, 64), address=None, **kw):
        self.halt = Event()

        if address is None:
            address = ('', 5566)

        self.canvas = Canvas(size, halt=self.halt)
        self.server = EcranServer(address, canvas=self.canvas)
        self.renderer = FlatRenderer(canvas=self.canvas, halt=self.halt)

    def start(self):
        self.canvas.start()
        self.server.start()
        self.renderer.start()

    def stop(self):
        self.halt.set()
        self.server.shutdown()
