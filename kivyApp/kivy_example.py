from kivy.app import App 
from kivy.uix.button import Button 
from kivy.config import Config 
class TestApp(App):
    """my first applicatioin class"""
    title='python kivy'
    def build(self):
        print(self.directory)
        print(self.config.get('section_1','key_1'))
        print(self.name)
        print('config',self.get_application_config())
        print(Config.get('kivy','log_level'))
        return Button(text=u"Hello World from kivy")

    def build_config(self,config):
        config.setdefaults("section_1",{"key_1":'123',"key_2":'456'})

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
