import numpy as np

from .base import Animation


class Rainbow(Animation):

    def __init__(self, direction=(1, 0), speed=1, **kw):
        super().__init__(**kw)
        self.d = np.array(direction)
        self.speed = speed

    def shade(self, out, mask, x):
        from .utils import hsv_to_rgb
        h = np.tensordot(x, self.d / mask.shape, (0, 0))
        out[..., 0] = (h - self.speed * self.passed) % 1
        out[..., 1] = 1
        out[..., 2] = 1
        return hsv_to_rgb(out), mask


class Gradient(Animation):

    def __init__(self, direction=(1, 0), **kw):
        super().__init__(**kw)
        self.d = np.array(direction)

    def shade(self, out, mask, x):
        v = np.tensordot(x, self.d, (0, 0))
        div = np.amax(v)
        if div:
            v /= div
        out[:] = v[..., np.newaxis] * self.color
        return out, mask
