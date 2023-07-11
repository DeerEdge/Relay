import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

#menu
from kivy.uix.widget import Widget

class Menu(BoxLayout):
    pass
#recycle view for home screen
class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.load_data()
        Clock.schedule_interval(self.load_data, 1)
    def load_data(self, *args):
        store = requests.get('http://127.0.0.1:8000/').json()

        list_data = []
        for item in store:
            list_data.append({'text': item['phone_number']})
        self.data = list_data
#screens
class HomeScreen(Screen):
    pass
class AddNewForm(Widget):
    text_input = ObjectProperty(None)

    input = StringProperty('')

    def submit_input(self):
        self.input = self.text_input.text
        post = requests.post('http://127.0.0.1:8000/add/', json={'phone_number': self.input})

        self.input = ''
class AddScreen(Screen):
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.box = BoxLayout()
        self.box.orientation = "vertical"
        self.box.add_widget(Label(text="Add To List...", color="blue",pos_hint={"top": 1}))
        self.addNewForm = AddNewForm()
        self.box.add_widget(self.addNewForm)
        self.add_widget(self.box)
#Screen Management
class ScreenManagement(ScreenManager):
    pass
#app class
class RelayApp(App):
    pass

if __name__ == '__main__':
    RelayApp().run()