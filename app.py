import asyncio
import socket
import threading
import time
from random import random
from multiprocessing import Process

from fsspec.asyn import loop
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

import receive_data_client
import send_data_client
import snippet_translate

Window.size = (360, 640)

Builder.load_file('login_window.kv')
Builder.load_file('calling_window.kv')
Builder.load_file('main_window.kv')

global kill_exec
kill_exec = False
recent_string = ""
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
        self.thread3 = threading.Thread(target=self.start_client)
        self.thread3.start()

    def start_call(self):
        self.wm.current = 'call'

    def start_client(self):
        receive_data_client.run()


    def activiate_whisper_translation(self):
        print("translate started")
        snippet_translate.main()

    def infiniteloop1(self):
        self.stopThreadHelper = threading.Event()
        while True:
            if self.stopThreadHelper.is_set():
                break
            print("____")
            time.sleep(5)

    def begin_record(self):
        self.createdThreads = True
        self.thread1 = threading.Thread(target=self.activiate_whisper_translation)
        self.thread2 = threading.Thread(target=self.infiniteloop1)
        self.thread1.start()
        self.thread2.start()

    def end_record(self):
        if self.createdThreads == True:
            print("nice transc")
            for line in snippet_translate.get_transciption():
                print(line)
            snippet_translate.stop_thread.set()
            self.stopThreadHelper.set()
            self.createdThreads = False
            print("threading ended")

    def end_call(self):
        if self.createdThreads == True:
            print("nice transc")
            for line in snippet_translate.get_transciption():
                print(line)
            snippet_translate.stop_thread.set()
            self.stopThreadHelper.set()
            self.createdThreads = False
            print("threading ended")

        self.wm.current = 'main'

MainApp().run()

# thread5 = threading.Thread(target=receive_data_client.run())
# thread6 = threading.Thread(target=MainApp().run())
# thread5.start()
# thread6.start()