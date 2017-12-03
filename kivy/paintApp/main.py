from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Line, BindTexture
from kivy.core.window import Window
from kivy.config import Config
from matplotlib import pyplot as plt
import numpy as np
from itertools import tee


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b, c, d = tee(iterable, 4)
    next(b, None)
    next(next(c, None), None)
    next(next(next(d, None), None), None)
    return zip(a, b, c, d)


class CanvasWidget(Widget):

    def on_touch_down(self, touch):
        # avoid painting line on button
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            # add line primitive
            Color(*get_color_from_hex("#0080FF80"))
            touch.ud['current_line'] = Line(
                points=(touch.x, touch.y), width=10)

    def on_touch_move(self, touch):
        if Widget.on_touch_down(self, touch):
            return
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)

    def clear_canvas(self):
        saved = self.children[:]  # copy by writing [:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)

    def show_info(self):
        all_pts = []
        for w in self.canvas.children:
            if isinstance(w, Line):
                all_pts += list(w.points)

        img = np.zeros((560+10, 560+10)).astype(np.uint8)
        xs = np.array(all_pts[::2]).astype(np.int)
        ys = np.array(all_pts[1::2]).astype(np.int)
        img[xs, ys] = 1
        plt.imshow(np.rot90(img))
        plt.show()


class PaintApp(App):

    def build(self):
        return CanvasWidget()


def main():
    Window.size = (560, 560)
    Config.set("input", "mouse", "mouse,disable_multitouch")
    Window.clearcolor = get_color_from_hex("#FFFFFF")
    PaintApp().run()

if __name__ == '__main__':
    main()
