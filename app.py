import threading
import time
from random import random
from multiprocessing import Process
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

import call_client
import snippet_translate

Window.size = (360, 640)

Builder.load_file('login_window.kv')
Builder.load_file('calling_window.kv')
Builder.load_file('main_window.kv')

global transcription
global old_string
global recent_string
global kill_exec

recent_string = ""
old_string = recent_string
kill_exec = False

class LoginWindow(Screen): pass

class MainWindow(Screen):
    def update_num_field(self, instance):
        if self.ids.number.text == "Enter Number":
            self.ids.number.text = ""
        self.ids.number.text = self.ids.number.text + instance.text
    def get_id(self, instance):
        for id, widget in instance.parent.ids.items():
            if widget.__self__ == instance:
                return id

class CallingWindow(Screen): pass

class WindowManager(ScreenManager): pass

class MainApp(MDApp):
    def build(self):
        self.createdThreads = False
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Light"

        self.wm = WindowManager()
        screens = [
            LoginWindow(name='login'), MainWindow(name='main'), CallingWindow(name='call')
        ]

        for screen in screens:
            self.wm.add_widget(screen)

        return self.wm

    def login(self):
        self.wm.current = 'main'

    def start_call(self):
        self.wm.current = 'call'
        call_client.run()

    def activiate_whisper_translation(self):
        print("translate started")
        snippet_translate.main()

    def infiniteloop1(self):
        self.stopThreadHelper = threading.Event()
        while True:
            if self.stopThreadHelper.is_set():
                break
            if recent_string != old_string:
                print(recent_string)
            time.sleep(5)

    def begin_record(self):
        self.createdThreads = True
        self.thread1 = threading.Thread(target=self.activiate_whisper_translation)
        self.thread2 = threading.Thread(target=self.infiniteloop1)
        self.thread1.start()
        self.thread2.start()

    def end_record(self):
        if self.createdThreads == True:
            snippet_translate.stop_thread.set()
            # self.stopThreadHelper.set()
            self.createdThreads = False
            print("threading ended")

    def end_call(self):
        if self.createdThreads == True:
            snippet_translate.stop_thread.set()
            self.stopThreadHelper.set()
            self.createdThreads = False
            print("threading ended")

        self.wm.current = 'main'

MainApp().run()