from kivy.config import Config
Config.set('graphics', 'width', 280)
Config.set('graphics', 'height', 280)
Config.set('graphics','resizable',0)
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Line, BindTexture
from matplotlib import pyplot as plt
import numpy as np
from scipy import interpolate

class CanvasWidget(Widget):

    def __init__(self):
        super(CanvasWidget, self).__init__()
        self.locked = False

    def on_touch_down(self, touch):
        # avoid painting line on button
        if Widget.on_touch_down(self, touch):
            return
        if self.locked:
            return

        with self.canvas:
            # add line primitive
            Color(*get_color_from_hex("#0080FF80"))
            touch.ud['current_line'] = Line(
                points=(touch.x, touch.y), width=10)

    def on_touch_move(self, touch):
        if Widget.on_touch_down(self, touch):
            return
        if self.locked:
            return
        print(touch.x,touch.y)
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)

    def clear_canvas(self):
        # copy children by writing [:]
        saved = self.children[:]

        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)

    def show_info(self):
        all_pts = []
        for w in self.canvas.children:
            if isinstance(w, Line):
                wpts=np.array(w.points)
                xs=wpts[::2]
                ys=wpts[1::2]
                tck,u=interpolate.splprep([xs,ys],s=0)
                u_new=np.arange(np.min(u),np.max(u),0.01)
                out=interpolate.splev(u_new,tck)
                print(out)
                all_pts += out

        img = np.zeros((560+10, 560+10)).astype(np.uint8)
        xs = np.array(all_pts[::2]).astype(np.int)
        ys = np.array(all_pts[1::2]).astype(np.int)
        img[xs, ys] = 1
        plt.imsave('hoge.png',img)

    def lock_draw(self):
        self.locked = not self.locked


class PaintApp(App):

    def build(self):
        return CanvasWidget()


def main():
    Config.set("input", "mouse", "mouse,disable_multitouch")
    Window.clearcolor = get_color_from_hex("#FFFFFF")
    PaintApp().run()

if __name__ == '__main__':
    main()
