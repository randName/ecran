from threading import Thread


class Renderer:

    default_interval = 1/24

    def __init__(self, canvas, interval=None, halt=None, **kw):
        if halt is not None:
            self.is_halted = halt.is_set
            self.stop = halt.set

            self._thread = Thread(target=self.run)

        self.canvas = canvas
        self.interval = interval or self.default_interval

    def is_halted(self):
        return False

    def start(self):
        self._thread.start()

    def stop(self):
        pass

    def run(self):
        from time import time, sleep
        last = time()
        while not self.is_halted():
            now = time()
            if now - last > self.interval:
                self.render()
                last = now
            else:
                sleep(self.interval / 10)

    def render(self):
        raise NotImplementedError


class FlatRenderer(Renderer):
    from pygame import display, mouse, surfarray

    def __init__(self, **kw):
        super().__init__(**kw)
        self.display.init()
        self.mouse.set_visible(False)

        self.size = self.canvas.array.shape[:2]
        self.screen = self.display.set_mode(self.size)
        self.screen.fill((0, 0, 0))
        self.start()

    def render(self):
        show = self.canvas.array[:, ::-1]
        self.surfarray.blit_array(self.screen, show)
        self.display.flip()
