import numpy as np


class Animation:
    """Base animation class"""

    def __init__(self, uid='', depth=0, fade=0, timeout=0, **kw):
        self.uid = uid
        self.depth = int(depth)

        try:
            fade = float(fade)
        except TypeError:
            fade = tuple(float(i) for i in fade)

        try:
            fade_in, fade_out = fade
        except TypeError:
            fade_in, fade_out = fade, fade

        self.fade_in = fade_in or 0
        self.fade_out = fade_out or 0
        self.alpha = 0 if self.fade_in > 0 else 1

        timeout = float(timeout)
        if not timeout and fade:
            timeout = self.fade_in + self.fade_out

        self.timeout = timeout
        self.remain = timeout
        self.passed = 0
        self.dt = 0
        self.t = 0

        color = kw.pop('color', (1, 1, 1))
        self.color = np.array(color, np.float32)
        self.params = kw

    def update(self, dt=None, t=None, **kw):
        try:
            fade = int(kw.pop('fade'))
            self.fade_out = fade
            self.remain = fade
        except (ValueError, KeyError):
            pass

        try:
            self.color = np.array(kw.pop('color'), np.float32)
        except (ValueError, KeyError):
            pass

        self.params.update(kw)

        if dt is None:
            return True

        self.passed += dt

        if self.fade_out and self.remain <= self.fade_out:
            self.alpha = self.remain / self.fade_out
        elif self.fade_in and self.alpha < 1:
            if self.passed >= self.fade_in:
                self.alpha = 1
            else:
                self.alpha = self.passed / self.fade_in

        if self.timeout and self.passed > self.timeout:
            return False

        if self.remain:
            self.remain -= dt
            if self.remain < 0:
                return False

        self.t = t
        self.dt = dt
        return True

    def shade(self, out, mask, x):
        raise NotImplementedError

    def __str__(self):
        return 'Animation <%s>' % self.uid


class Solid(Animation):

    def __init__(self, **kw):
        super().__init__(**kw)

    def shade(self, out, mask, x):
        out[:] = self.color
        return out, mask


class Random(Animation):

    def __init__(self, **kw):
        super().__init__(**kw)

    def shade(self, out, mask, x):
        return np.random.random(out.shape), mask
