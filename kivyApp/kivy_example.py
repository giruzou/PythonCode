from kivy.app import App 
from kivy.uix.button import Button 

class TestApp(App):
    """my first applicatioin class"""
    def build(self):
        return Button(text= "Hello World from kivy")

def main():
    TestApp().run()

if __name__ == '__main__':
    main()
