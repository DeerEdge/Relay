from random import random

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (360, 640)

class LoginWindow(Screen):
    pass


class MainWindow(Screen):
    def update_num_field(self, instance):
        if self.ids.number.text == "Enter Number":
            self.ids.number.text = ""
        self.ids.number.text = self.ids.number.text + instance.text

    def get_id(self, instance):
        for id, widget in instance.parent.ids.items():
            if widget.__self__ == instance:
                return id

class CallingWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Light"

        self.root_widget = Builder.load_file('layout.kv')
        return self.root_widget

    def login(self):
        self.root_widget.current = 'main'

    def start_call(self):
        self.root_widget.current = 'call'

    def end_call(self):
        self.root_widget.current = 'main'

MainApp().run()