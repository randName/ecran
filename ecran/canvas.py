from threading import Thread

import numpy as np


class Canvas:
    """Raw color data and animation handler"""

    fps_interval = 2
    default_interval = 1/24

    def __init__(self, size, interval=None, halt=None):
        self.size = size
        self.len = np.prod(self.size)
        self.array = np.zeros(size + (3,), np.uint8)
        self.index = np.indices(self.array.shape[:-1], np.float32)

        self.fps = 0
        self.frames = 0
        self.interval = interval or self.default_interval
        self.animations = []

        if halt is not None:
            self.is_halted = halt.is_set
            self.stop = halt.set

        self._task = Thread(target=self._run)
        self._task.start()

    def is_halted(self):
        return False

    def stop(self):
        pass

    def _run(self):
        from time import time, sleep
        last = time()
        last_fps = last
        while not self.is_halted():
            now = time()
            dt = now - last
            df = now - last_fps

            if df >= self.fps_interval:
                self.fps = self.frames / df
                self.frames = 0
                last_fps = now

            if dt > self.interval:
                self.array = self.render(dt, now)
                self.frames += 1
                last = now
            else:
                sleep(self.interval / 10)

    @property
    def shape(self):
        return self.array.shape

    @property
    def blank(self):
        return np.zeros(self.shape, np.float32)

    @property
    def mask(self):
        return np.ones(self.size, np.uint8)

    def clear(self):
        self.animations.clear()

    def add(self, a):
        self.animations.append(a)
        self.animations.sort(key=lambda a: a.depth)

    def update(self, name, params):
        try:
            ani = next(a for a in self.animations if a.uid == name)
            ani.update(**params)
        except StopIteration:
            pass

    def render(self, dt, t):
        self.animations = [a for a in self.animations if a.update(dt, t)]
        if not self.animations:
            return np.zeros(self.shape, np.uint8)

        bg = self.blank
        for a in self.animations:
            fg, mask = a.shade(self.blank, self.mask, self.index)
            fg *= a.alpha
            cover = mask > 0
            bg[cover] = fg[cover]
        return (bg * 255).astype(np.uint8)
