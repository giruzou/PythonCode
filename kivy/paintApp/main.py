from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Line
from kivy.config import Config


class CanvasWidget(Widget):

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self,touch):
            return
        with self.canvas:
            Color(*get_color_from_hex("#0080FF80"))
            touch.ud['current_line']=Line(
                points=(touch.x,touch.y),width=10)

    def on_touch_move(self,touch):
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points+=(touch.x,touch.y)

class PaintApp(App):

    def build(self):
        return CanvasWidget()


def main():
    Config.set("graphics", "width", '960')
    Config.set("graphics", "height", '540')
    Config.set("input","mouse","mouse,disable_multitouch")
    Window.clearcolor = get_color_from_hex("#FFFFFF")
    PaintApp().run()

if __name__ == '__main__':
    main()
