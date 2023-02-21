from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import json
import pandas
import random
from kivy.clock import mainthread
from difflib import SequenceMatcher

Builder.load_file("main.kv")

'''
d = {"test english" : "test Turkish", "test1" : "test2"}
data = pandas.DataFrame.from_dict(d, orient = "index", dtype = None, columns = ["."])
data.to_json("Vocabulary.json")
'''
'''
d = {"font_size" : "20px"}
with open("settings.json", "w") as file:
    json.dump(d, file, indent = 1)
'''

def similar(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

def lowercase_turkish(str_U):
    str_l = ""
    for char in str_U:
        if char != "I" and char != "İ":
            str_l += char.lower()
        elif char == "I":
            str_l += "ı"
        elif char == "İ":
            str_l += "i"
    return str_l


class Blank(Screen):
    @mainthread
    def on_enter(self, *args):
        self.manager.current = "main_menu"


class MainMenu(Screen):
    def go_to(self, page):
        self.manager.current = page


class Setting(Screen):
    def go_to(self, page):
        self.manager.current = page

    def apply(self):
        try:
            self.ids.warning.text = ""

            if len(str(self.ids.font_input.text)) != 0:
                new_size = int(self.ids.font_input.text)

                with open("settings.json", "r") as file:
                    data = json.load(file)
                    data["font_size"] = f"{new_size}px"
                    with open("settings.json", "w") as file_1:
                        json.dump(data, file_1, indent = 1)

            MainApp().stop()

        except:
            self.ids.warning.text = "Enter a valid Number"


class VocCards(Screen):
    data = {}
    count = 0
    randomizing = False

    def on_pre_enter(self, *args):
        pass

    def on_enter(self):
        d = pandas.read_json("Vocabulary.json")
        self.data = d.to_dict()["."]
        self.randomize(None)

    def go_to(self, page):
        self.manager.current = page

    def answer(self):
        if not self.randomizing:
            if lowercase_turkish(self.data[str(self.ids.English.text)]) == lowercase_turkish(str(self.ids.Turkish.text)):
                Clock.schedule_once(self.randomize, 2)
                self.randomizing = True
                self.ids.right_or_wrong.color = '#00FF00'
                self.ids.right_or_wrong.text = "Correct!"
            elif similar(lowercase_turkish(self.data[str(self.ids.English.text)]), lowercase_turkish(str(self.ids.Turkish.text))) > 0.7:
                Clock.schedule_once(self.randomize, 2)
                self.randomizing = True
                self.ids.right_or_wrong.color = '#00FF00'
                self.ids.right_or_wrong.text = f"Correct!\nThe answer is: {self.data[str(self.ids.English.text)]}"
            elif self.count < 3:
                self.ids.right_or_wrong.color = '#FF0000'
                self.count += 1
                self.ids.right_or_wrong.text = f"WRONG!\nIncorrect Attempts: {self.count}"
            else:
                self.ids.right_or_wrong.color = '#FF0000'
                self.ids.right_or_wrong.text = f"WRONG!\nThe answer is: {self.data[str(self.ids.English.text)]}"
                self.randomizing = True
                Clock.schedule_once(self.randomize, 2)


    def randomize(self, dt):
        self.randomizing = False
        self.count = 0
        self.ids.Turkish.text = ""
        self.ids.right_or_wrong.text = ""
        self.ids.English.text = random.sample(self.data.keys(), 1)[0]


    def on_leave(self, *args):
        del self.data


class Editor(Screen):
    data = {}
    buttons = []
    to_be_edited = ""
    edit_mode = False
    add_mode = True
    screen = None

    def on_pre_enter(self, *args):
        self.data = pandas.read_json("Vocabulary.json").to_dict()["."]
        Editor.screen = self

    @mainthread
    def on_enter(self, *args):
        for row in self.data.keys():
            self.build_widgets(row)


    def build_widgets(self, word):
        english = MainLabel(text = word, size_hint_y = None)
        turkish = MainLabel(text = self.data[word], size_hint_y = None)
        edit_button = ScrollButton(text=f"\nEdit\n[color=#00000000]{word}[/color]", size_hint_y = None, markup = True)
        self.ids.grid.add_widget(english)
        self.ids.grid.add_widget(turkish)
        self.ids.grid.add_widget(edit_button)
        self.buttons.append([english, turkish, edit_button])

    def go_to(self, page):
        self.manager.current = page


    def start_edit(self, w):
        self.start_edit_workaround(w)


    def start_edit_workaround(self, w):
        self.add_mode = False
        self.edit_mode = True
        word = w[23:].replace("[/color]", "")
        self.to_be_edited = word
        self.ids.English.text = word
        self.ids.old_English.text = word
        self.ids.Turkish.text = self.data[word]
        self.ids.old_Turkish.text = self.data[word]


    def edit(self):
        if self.edit_mode and len(str(self.ids.English.text)) > 0 and len(str(self.ids.Turkish.text)) > 0:
            new_english = str(self.ids.English.text)
            new_turkish = str(self.ids.Turkish.text)
            self.data[new_english] = new_turkish
            self.edit_mode = False
            self.add_mode = True

            del self.data[self.to_be_edited]
            pandas.DataFrame.from_dict(self.data, orient = "index", dtype = None, columns = ["."]).to_json("Vocabulary.json")
            self.data = pandas.read_json("Vocabulary.json").to_dict()["."]

            for row in self.buttons:
                if str(row[0].text) == self.to_be_edited:
                    row[0].text = new_english
                    row[1].text = self.data[new_english]
                    row[2].text = f"\nEdit\n[color=#00000000]{new_english}[/color]"

            self.ids.English.text = ""
            self.ids.old_English.text = ""
            self.ids.Turkish.text = ""
            self.ids.old_Turkish.text = ""


    def add(self):
        if self.add_mode and len(str(self.ids.English.text)) > 0 and len(str(self.ids.Turkish.text)) > 0 and str(self.ids.English.text) not in self.data.keys() and str(self.ids.Turkish.text) not in self.data.values():
            new_english = str(self.ids.English.text)
            new_turkish = str(self.ids.Turkish.text)
            self.data[new_english] = new_turkish

            pandas.DataFrame.from_dict(self.data, orient = "index", dtype = None, columns = ["."]).to_json("Vocabulary.json")
            self.data = pandas.read_json("Vocabulary.json").to_dict()["."]
            self.build_widgets(new_english)

            self.ids.English.text = ""
            self.ids.old_English.text = ""
            self.ids.Turkish.text = ""
            self.ids.old_Turkish.text = ""
        else:
            if str(self.ids.English.text) in self.data.keys():
                self.ids.old_English.text = f"{str(self.ids.English.text)} is already added."
            if str(self.ids.Turkish.text) in self.data.values():
                self.ids.old_Turkish.text = f"{str(self.ids.Turkish.text)} is already added."


    def delete(self):
        if self.edit_mode and len(str(self.ids.English.text)) > 0 and len(str(self.ids.Turkish.text)) > 0:
            del self.data[self.to_be_edited]
            pandas.DataFrame.from_dict(self.data, orient="index", dtype=None, columns=["."]).to_json("Vocabulary.json")
            self.data = pandas.read_json("Vocabulary.json").to_dict()["."]

            for row in self.buttons:
                if str(row[0].text) == self.to_be_edited:
                    for wid in row:
                        self.ids.grid.remove_widget(wid)
                    del row

            self.ids.English.text = ""
            self.ids.old_English.text = ""
            self.ids.Turkish.text = ""
            self.ids.old_Turkish.text = ""

    def reset(self):
        self.to_be_edited = ""
        self.ids.English.text = ""
        self.ids.old_English.text = ""
        self.ids.Turkish.text = ""
        self.ids.old_Turkish.text = ""

        self.add_mode = True
        self.edit_mode = False

    @mainthread
    def on_leave(self, *args):
        for row in self.buttons:
            for widget in row:
                self.ids.grid.remove_widget(widget)

        self.data = {}
        self.buttons = []


class MainButton(Button):
    pass


class ScrollButton(MainButton):
    def on_release(self):
        return Editor.screen.start_edit(str(self.text))


class MainLabel(Label):
    pass


class MainSpinner(Spinner):
    pass


class MainTextInput(TextInput):
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()