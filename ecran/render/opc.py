import socket as sk
from struct import pack
from .base import Renderer

GRB2RGB = (..., (1, 0, 2))


class OPCRenderer(Renderer):

    def __init__(self, address, layout, start=True, **kw):
        super().__init__(**kw)

        self.address = address
        self.layout = layout
        self._socket = None

        if start:
            self.start()

    def send(self, packet):
        if self._socket is None:
            try:
                self._socket = sk.socket()
                self._socket.connect(self.address)
                self._socket.setblocking(False)
                self._socket.setsockopt(sk.IPPROTO_TCP, sk.TCP_NODELAY, True)
            except OSError:
                self._socket = None

        if self._socket is not None:
            try:
                self._socket.send(packet)
                return True
            except OSError:
                self._socket = None

        return False

    def close(self):
        if self._socket:
            self._socket.close()
        self._socket = None

    def put_pixels(self, pixels, channel=0):
        header = pack('>BBH', channel, 0, len(pixels))
        self.send(header + pixels)

    def render(self):
        pixels = self.canvas.array[GRB2RGB][self.layout].tobytes()
        self.put_pixels(pixels)
