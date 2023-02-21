from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import mainthread, Clock

from datetime import datetime
from Plotter import plot

Builder.load_file('main.kv')

class Blank(Screen):
    # to ensure all screen names have been identified by kivy
    @mainthread
    def on_enter(self, *args):
        self.manager.current = "map"

class Map(Screen):
    # ids: {Mlabels: [time], RoomButtons: [A1, A2, A3]}
    def on_enter(self, *args):
        # schedules self.time to refresh once per second
        self.time(None)
        Clock.schedule_interval(self.time, 1)

    def time(self, dt):
        # updates the clock at the top left of the screen
        self.ids.time.text = datetime.now().strftime("%I:%M:%S %p")

    def on_pre_leave(self, *args):
        # to prevent unnecessary functions to be taking place
        Clock.unschedule(self.time)

class Plot(Screen):
    # ids: {Mlabels: [time], Images: [plot]}
    def on_enter(self, *args):
        # schedules self.time to refresh once per second
        self.time(None)
        Clock.schedule_interval(self.time, 1)

    def time(self, dt):
        # updates the clock at the top left of the screen
        self.ids.time.text = datetime.now().strftime("%I:%M:%S %p")

    def on_pre_leave(self, *args):
        # to prevent unnecessary functions to be taking place
        Clock.unschedule(self.time)

class RootWidget(ScreenManager):
    pass

class Mbutton(Button):
    pass

class MtextInput(TextInput):
    pass

class Mlabel(Label):
    pass

class RoomButton(Button):
    def on_release(self):
        pass

class FloorButton(Button):
    pass

class RoomPopup(GridLayout):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()