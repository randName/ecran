from threading import Event

from .canvas import Canvas
from .render import FlatRenderer


class Ecran:
    """Ecran server and renderer"""

    def __init__(self, size=(256, 64), **kw):
        self.halt = Event()

        self.canvas = Canvas(size, halt=self.halt)
        self.renderer = FlatRenderer(canvas=self.canvas, halt=self.halt)

    def start(self):
        self.canvas.start()
        self.renderer.start()

    def stop(self):
        self.halt.set()
