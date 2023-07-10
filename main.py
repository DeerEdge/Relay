from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (360, 640)

class MainApp(MDApp):
    def build(self):
        return Builder.load_file('layout.kv')

MainApp().run()