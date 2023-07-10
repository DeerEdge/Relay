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

class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):

    def build(self):
        self.root_widget = Builder.load_file('layout.kv')
        return self.root_widget

    def login(self, dt):
        self.root_widget.current = 'main'

MainApp().run()