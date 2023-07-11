import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import OneLineAvatarIconListItem
from demo.demo import profiles
import demo.group
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.widget import Widget

Window.size = (360, 640)

Builder.load_file('widgets/avatar.kv')
Builder.load_file('widgets/chat_list_item.kv')
Builder.load_file('widgets/group_list_item.kv')
Builder.load_file('widgets/call_list_item.kv')
Builder.load_file('widgets/bottom_navigator.kv')
Builder.load_file('widgets/text_field.kv')
Builder.load_file('widgets/chatbubble.kv')
Builder.load_file('layout.kv')

class ChatScreen(Screen):
    '''A screen that display messages with a user.'''

    text = StringProperty()
    image = ObjectProperty()
    active = BooleanProperty(defaultvalue=False)

class StoryWithImage(MDBoxLayout):
    '''A horizontal layout with an image(profile picture)
        and a text(username) - The Story.'''

    text = StringProperty()
    source = StringProperty()

class ChatListItem(MDCard):
    '''A clickable chat item for the chat timeline.'''

    isRead = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting'])
    friend_name = StringProperty()
    mssg = StringProperty()
    timestamp = StringProperty()
    friend_avatar = StringProperty()
    profile = DictProperty()

class GroupListItem(MDCard):
    '''A clickable chat item for the group chat timeline.'''

    isRead = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting'])
    group_name = StringProperty()
    group_avatar = StringProperty()
    friend_mssg = StringProperty()
    timestamp = StringProperty()

class ChatBubble(MDBoxLayout):
    '''A chat bubble for the chat screen messages.'''

    profile = DictProperty()
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()
    isRead = OptionProperty('waiting', options=['read', 'delivered', 'waiting'])

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

        # self.root_widget = Builder.load_file('layout.kv')
        # return self.root_widget

        self.wm = WindowManager(transition=FadeTransition())
        screens = [
            LoginWindow(name='login'), MainWindow(name='main'), CallingWindow(name='call')
        ]
        for screen in screens:
            self.wm.add_widget(screen)

        # self.story_builder()
        # self.chatlist_builder()
        # self.grouplist_builder()

        return self.wm

    def login(self):
        self.wm.current = 'main'

    def start_call(self):
        self.wm.current = 'call'

    def end_call(self):
        self.wm.current = 'main'

MainApp().run()