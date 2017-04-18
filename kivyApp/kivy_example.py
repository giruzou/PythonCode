from kivy.app import App 
from kivy.uix.button import Button 

class TestApp(App):
    """my first applicatioin class"""
    title='python kivy'
    def build(self):
        return Button(text= "Hello World from kivy")

    def on_start(self):
        print("----")
        print("on start")
        print("----")
        
    def on_stop(self):
        print("----")
        print("on stop")
        print("----")

def main():
    TestApp().run()

if __name__ == '__main__':
    main()
