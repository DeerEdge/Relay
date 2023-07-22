import socket
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

    def start_call(self):
        self.wm.current = 'call'


    def start_client(self):
        HEADER_LENGTH = 10

        # IP Address of the server
        IP = "192.168.1.42"
        PORT = 1234
        my_username = "DV"
        # my_username = input("Username: ")

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        client_socket.connect((IP, PORT))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)

        while True:
            message = snippet_translate.get_recent_string()
            print("Message" + message)

            # If message is not empty - send it
            if message:
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)

            time.sleep(0.25)

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