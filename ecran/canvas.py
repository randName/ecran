import numpy as np


class Canvas:
    """Raw color data and animation handler"""

    default_interval = 1/24

    def __init__(self, size, interval=None, halt=None):
        self.size = size
        self.len = np.prod(self.size)
        self.array = np.zeros(size + (3,), np.uint8)
        self.index = np.indices(self.array.shape[:-1], np.float32)

        self.interval = interval or self.default_interval
        self.animations = []

        if halt is not None:
            self.is_halted = halt.is_set
            self.stop = halt.set

            from threading import Thread
            self.update_thread = Thread(target=self.run)

    def is_halted(self):
        return False

    def run(self):
        from time import time, sleep
        last = time()
        while not self.is_halted():
            now = time()
            dt = now - last
            if dt > self.interval:
                self.update(dt, now)
                last = now
            else:
                sleep(self.interval / 10)

    def start(self):
        self.update_thread.start()

    def stop(self):
        pass

    @property
    def shape(self):
        return self.array.shape

    @property
    def blank(self):
        return np.zeros(self.shape, np.float32)

    @property
    def mask(self):
        return np.ones(self.size, np.uint8)

    def add(self, a):
        self.animations.append(a)
        self.animations.sort(key=lambda a: a.depth)

    def update(self, dt, t):
        self.animations = [a for a in self.animations if a.update(dt, t)]
        if not self.animations:
            self.array = np.zeros(self.shape, np.uint8)
            return

        bg = self.blank
        for a in self.animations:
            fg, mask = a.shade(self.blank, self.mask, self.index)
            fg *= a.alpha
            cover = mask > 0
            bg[cover] = fg[cover]
        self.array = (bg * 255).astype(np.uint8)

    def __len__(self):
        return self.len
