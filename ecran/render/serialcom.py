from numpy import full_like, minimum

from .base import Renderer

LED_HEADER = bytes((0xFF, 0xFF))


class SerialRenderer(Renderer):

    def __init__(self, port='/dev/ttyUSB0', baud=400000, tout=1, **kw):
        from serial import Serial
        super().__init__(**kw)

        self.clamp = full_like(self.canvas.array, 0xFE)
        self.port = port
        self.serial = Serial(port=port, baudrate=baud, timeout=tout)
        self.reset()
        self.start()

    def render(self):
        raw = minimum(self.canvas.array, self.clamp)
        self.write(LED_HEADER)
        self.write(raw.tobytes())

    def reset(self):
        self.serial.dtr = False
        self.serial.reset_input_buffer()
        self.serial.dtr = True
        self.serial.read(1)

    def write(self, data):
        return self.serial.write(data)
