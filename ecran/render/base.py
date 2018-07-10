from threading import Thread


class Renderer:

    default_interval = 1/48

    def __init__(self, canvas, interval=None, halt=None, **kw):
        if halt is not None:
            self.is_halted = halt.is_set
            self.stop = halt.set

        self._thread = Thread(target=self._run)

        self.canvas = canvas
        self.interval = interval or self.default_interval

    def is_halted(self):
        return False

    def start(self):
        self._thread.start()

    def stop(self):
        pass

    def _run(self):
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


class SimpleRenderer(Renderer):

    def __init__(self, render=None, **kw):
        super().__init__(**kw)
        if render is not None:
            self.render = render
        self.start()

    def render(self):
        pass


class MultiRenderer(Renderer):

    def __init__(self, renderers, **kw):
        super().__init__(**kw)

        self.renderers = []
        for r in renderers:
            try:
                r, k = r
            except TypeError:
                k = {}
            self.renderers.append(r(canvas=self.canvas, start=False, **k))
        self.start()

    def render(self):
        for r in self.renderers:
            r.render()
