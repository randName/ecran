import numpy as np


def hsv_to_rgb(hsv):
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    f = h * 6
    i = f.astype(np.int32)
    f -= i
    i = i % 6

    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    cc = ((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))

    rgb = np.zeros_like(hsv)
    for l, z in enumerate(cc):
        hp = i == l
        rgb[hp] = np.dstack(z)[hp]
    return rgb
