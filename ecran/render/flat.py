from pygame import display, mouse, surfarray

from .base import Renderer


class FlatRenderer(Renderer):

    def __init__(self, start=True, **kw):
        super().__init__(**kw)
        display.init()
        mouse.set_visible(False)

        self.size = self.canvas.array.shape[:2]
        self.screen = display.set_mode(self.size)
        self.screen.fill((0, 0, 0))

        if start:
            self.start()

    def render(self):
        show = self.canvas.array[:, ::-1]
        surfarray.blit_array(self.screen, show)
        display.flip()
