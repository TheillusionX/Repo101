from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex as hex
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.graphics import RoundedRectangle
import random
import json

Builder.load_file("main_menu.kv")
selected_numbers_list = []
all_numbers_selected = False

decimal_numbers = [x for x in range(1, 11)]

round_number = 10
time_per_round = 10

class Blank(Screen):
    counter = None

    def on_enter(self, *args):
        Blank.counter = Clock.schedule_interval(self.start, 0.5)

    def start(self, dt):
        self.manager.current = "main_menu"

    def on_leave(self, *args):
        Blank.counter.cancel()


class MainMenu(Screen):
    selected_game_mode = "Guess The Product!"
    difficulty_coefficient = 1

    def on_pre_enter(self, *args):
        global selected_numbers_list

        buttons_list = [self.ids.button_1, self.ids.button_2, self.ids.button_3, self.ids.button_4, self.ids.button_5, self.ids.button_6, self.ids.button_7, self.ids.button_8, self.ids.button_9]
        if SettingsPage.difficulty == "hard":
            for button, number in zip(buttons_list, range(11, 21)):
                button.text = str(number)
                button.opacity = 0.4

        else:
            for button, number in zip(buttons_list, range(1, 11)):
                button.text = str(number)
                button.opacity = 0.4

        for button in buttons_list:
            if int(button.text) in selected_numbers_list:
                button.color = (1 - hex(SettingsPage.button_color[0])[0], 1 - hex(SettingsPage.button_color[0])[1], 1 - hex(SettingsPage.button_color[0])[2], button.color[3])
                button.opacity = 1
            else:
                button.color = [0, 0, 0, 1] if SettingsPage.button_color[0] != "#0000ff" else [1, 1, 1, 1]
                button.opacity = 0.4

    def select_number(self, button):
        if int(button.text) in selected_numbers_list:
            selected_numbers_list.remove(int(button.text))
            button.color = hex('#000000') if SettingsPage.button_color[0] != "#0000ff" else hex('#FFFFFF')
            button.opacity = 0.5
        else:
            selected_numbers_list.append(int(button.text))
            button.color = (1 - hex(SettingsPage.button_color[0])[0], 1 - hex(SettingsPage.button_color[0])[1], 1 - hex(SettingsPage.button_color[0])[2], button.color[3])
            button.opacity = 1

    def toggle_select_all_numbers(self):
        buttons_list = [self.ids.button_1, self.ids.button_2, self.ids.button_3, self.ids.button_4, self.ids.button_5, self.ids.button_6, self.ids.button_7, self.ids.button_8, self.ids.button_9]

        for button in buttons_list:
            self.select_number(button)

    def select_game_mode(self, game_mode):
        MainMenu.selected_game_mode = game_mode
        self.ids.label_game_mode.text = f"Selected game mode: {game_mode}"

    def start_game(self):
        global selected_numbers_list, round_number, time_per_round, decimal_numbers
        if len(selected_numbers_list) != 0 or all_numbers_selected:

            games_dict = {"Guess The Product!" : "game_one", "Write The Product!" : "game_two", "Guess The Factor!": "game_three"}

            point_index = str(self.ids.label_game_mode.text).index("!")
            self.ids.label_game_mode.text = self.ids.label_game_mode.text[0: point_index + 1]

            difficulty = json.load(open("preferences.txt", "r"))["difficulty"]
            if difficulty == "hard" or difficulty == "medium":
                decimal_numbers = [x for x in range(1, 21)]
            else:
                decimal_numbers = [x for x in range(1, 11)]

            if difficulty == "hard":
                MainMenu.difficulty_coefficient = 1.5
            elif difficulty == "medium":
                MainMenu.difficulty_coefficient = 1.25
            else:
                pass

            try:
                round_number = int(self.ids.round_number.text)
            except:
                round_number = 10

            try:
                time_per_round = int(self.ids.seconds_per_round.text)
            except:
                time_per_round = 10

            self.manager.current = games_dict[MainMenu.selected_game_mode]

        else:
            point_index = str(self.ids.label_game_mode.text).index("!")
            self.ids.label_game_mode.text = self.ids.label_game_mode.text[0 : point_index + 1]
            self.ids.label_game_mode.text += "\nChoose at least one number!"

    def to_settings(self):
        self.manager.current = "settings"

class SettingsPage(Screen):

    preferences = json.load(open("preferences.txt", "r"))

    font_size = preferences["font_size"]
    button_color = preferences["button_color"]
    roundness = preferences["roundness"]
    difficulty = preferences["difficulty"]
    new_difficulty = None

    delete_after_wrong = preferences["delete_after_wrong"]
    delete_option_text = ""
    if delete_after_wrong:
        delete_option_text = "Delete"
    else:
        delete_option_text = "Do not delete"

    settings_changed = False

    def on_pre_enter(self, *args):
        self.ids.apply_changes.opacity = 0.2
        SettingsPage.preferences = json.load(open("preferences.txt", "r"))

        SettingsPage.font_size = SettingsPage.preferences["font_size"]
        SettingsPage.button_color = SettingsPage.preferences["button_color"]
        SettingsPage.roundness = SettingsPage.preferences["roundness"]
        SettingsPage.difficulty = SettingsPage.preferences["difficulty"]

        SettingsPage.delete_after_wrong = SettingsPage.preferences["delete_after_wrong"]

    def on_enter(self, *args):
        buttons_list = [self.ids.easy, self.ids.medium, self.ids.hard]

        for button in buttons_list:
            if str(button.text).lower() == SettingsPage.difficulty:
                with button.canvas.before:
                    Color(rgba = hex(SettingsPage.button_color[1]))
                    RoundedRectangle(pos = button.pos, size = button.size, radius = [int(SettingsPage.roundness)] * 4)
            else:
                with button.canvas.before:
                    Color(rgba = hex(SettingsPage.button_color[0]))
                    RoundedRectangle(pos = button.pos, size = button.size, radius = [int(SettingsPage.roundness)] * 4)

        button = self.ids.toggle_delete_after_wrong
        with button.canvas.before:
            if SettingsPage.delete_after_wrong:
                Color(rgba = (0, 1, 0, 1))
            else:
                Color(rgba = (1, 0, 0, 1))
            RoundedRectangle(pos = button.pos, size = button.size, radius = [int(SettingsPage.roundness)] * 4)

    def return_to_main(self):
        self.manager.current = "main_menu"

    def num_only(self, text):
        SettingsPage.settings_changed = True
        self.ids.apply_changes.opacity = 1
        try:
            int(text)
            self.ids.difficulty_description.text = str(self.ids.difficulty_description.text).replace("\nNumbers only for font size and roundness!", "")
        except:
            if len(text) != 0:
                self.ids.difficulty_description.text = str(self.ids.difficulty_description.text).replace("\nNumbers only for font size and roundness!", "")
                self.ids.difficulty_description.text += "\nNumbers only for font size and roundness!"
            else:
                self.ids.difficulty_description.text = str(self.ids.difficulty_description.text).replace("\nNumbers only for font size and roundness!", "")

    def apply_changes(self, new_size, new_radius):
        if SettingsPage.settings_changed:
            self.update_font_size(new_size)
            self.update_roundness(new_radius)
            self.update_difficulty(SettingsPage.new_difficulty)
            self.update_color()
            SettingsPage.settings_changed = False

            content = ExitApp()
            pop = Popup(title = "", content = content, size_hint = [0.75, 0.3], background = 'white.png', auto_dismiss = True)
            pop.open()

    def update_font_size(self, new_size):
        try:
            new_size = str(int(new_size))
            with open("preferences.txt", "r") as file:
                data = json.load(file)
                if int(new_size) < 100:
                    data["font_size"] = f"{new_size}px"
                else:
                    data["font_size"] = f"300px"
                with open("preferences.txt", "w") as file_1:
                    json.dump(data, file_1, indent = 1)
        except:
            pass

    def choose_color(self, instance):
        content = ColorPopup()
        pop = Popup(title = "Choose a Color", title_color = [0, 0, 0], content = content, size_hint = [0.75, 0.3], background = 'white.png', auto_dismiss = True, on_dismiss = self.update_color_button)
        pop.open()

    def update_color_button(self, instance):
        try:
            SettingsPage.settings_changed = True
            self.ids.apply_changes.opacity = 1
            with self.ids.color_display.canvas.before:
                Color(rgb = hex(ColorPopup.new_colors[0]))
                RoundedRectangle(pos = self.ids.color_display.pos, size = self.ids.color_display.size, radius = [int(SettingsPage.roundness)] * 4)
        except:
            pass

    def update_color(self):
        if len(ColorPopup.new_colors) != 0:
            with open("preferences.txt", "r") as file:
                data = json.load(file)
                data["button_color"] = ColorPopup.new_colors
                with open("preferences.txt", "w") as file_1:
                    json.dump(data, file_1, indent=1)

    def update_roundness(self, new_radius):
        try:
            new_radius = str(int(new_radius))
            with open("preferences.txt", "r") as file:
                data = json.load(file)
                data["roundness"] = f"{new_radius}"
                with open("preferences.txt", "w") as file_1:
                    json.dump(data, file_1, indent = 1)
        except:
            pass

    def toggle_delete_after_wrong(self):
        SettingsPage.delete_after_wrong = not SettingsPage.delete_after_wrong
        button = self.ids.toggle_delete_after_wrong
        SettingsPage.settings_changed = True
        self.ids.apply_changes.opacity = 1

        with button.canvas.before:
            if SettingsPage.delete_after_wrong:
                Color(rgba = (0, 1, 0, 1))
                button.text = "Delete"
            else:
                Color(rgba = (1, 0, 0, 1))
                button.text = "Do not delete"
            RoundedRectangle(pos = button.pos, size = button.size, radius = [int(SettingsPage.roundness)] * 4)

        with open("preferences.txt", "r") as file:
            data = json.load(file)
            data["delete_after_wrong"] = SettingsPage.delete_after_wrong
            with open("preferences.txt", "w") as file_1:
                json.dump(data, file_1, indent = 1)

    def display_difficulty(self, instance):
        buttons_list = [self.ids.easy, self.ids.medium, self.ids.hard]
        SettingsPage.settings_changed = True
        self.ids.apply_changes.opacity = 1

        SettingsPage.new_difficulty = str(instance.text).lower()
        SettingsPage.difficulty = str(instance.text).lower()
        with instance.canvas.before:
            Color(rgba = hex(SettingsPage.button_color[1]))
            RoundedRectangle(pos = instance.pos, size = instance.size, radius = [int(SettingsPage.roundness)])

        buttons_list.remove(instance)
        self.ids.difficulty_description.text = SettingsPage.preferences[str(instance.text).lower()]

        for button in buttons_list:
            with button.canvas.before:
                Color(rgba = hex(SettingsPage.button_color[0]))
                RoundedRectangle(pos=button.pos, size=button.size, radius=[int(SettingsPage.roundness)])

    def update_difficulty(self, new_difficulty):
        global selected_numbers_list
        selected_numbers_list = []

        if new_difficulty is not None:
            with open("preferences.txt", "r") as file:
                data = json.load(file)
                data["difficulty"] = new_difficulty
                with open("preferences.txt", "w") as file_1:
                    json.dump(data, file_1, indent = 1)

class ColorPopup(GridLayout):

    new_colors = []

    def choose_color(self, colors):
        ColorPopup.new_colors = [colors[0:7], colors[8:]]

class ExitApp(GridLayout):
    def restart(self):
        MainApp().get_running_app().stop()


class GameOneScreen(Screen):
    counter = None

    current_round_number = 0

    correct = 0
    incorrect = 0
    score = 0

    answered = False

    factor_one = 0
    factor_two = 0

    def on_pre_enter(self, *args):

        GameOneScreen.current_round_number = 0
        GameOneScreen.correct = 0
        GameOneScreen.incorrect = 0
        GameOneScreen.score = 0.0

        self.ids.counter.text = str(time_per_round)
        self.add_to_clock(None)
        self.generate_question()

    def add_to_clock(self, dt):
        if self.manager.current == "game_one":
            GameOneScreen.counter = Clock.schedule_interval(self.decrease_counter, 1)

    def remove_from_clock(self):
        if self.manager.current == "game_one":
            GameOneScreen.counter.cancel()

    def decrease_counter(self, dt):

        if int(self.ids.counter.text) != 0:
            self.ids.counter.text = str(int(self.ids.counter.text) - 1)
        else:
            self.ids.display_correct.color = hex('#FF0000')
            self.ids.display_correct.text = "TIME OUT!"
            self.generate_question()
            GameOneScreen.answered = True

            GameOneScreen.incorrect += 1
            GameOneScreen.score -= 20

    def return_to_main(self):
        GameOneScreen.answered = False
        self.reset_buttons()
        self.remove_from_clock()
        self.manager.current = "main_menu"

    def answer(self, button_id):
        if not GameOneScreen.answered:
            if int(button_id.text) == int(GameOneScreen.factor_one) * int(GameOneScreen.factor_two):
                button_id.color = hex('#48ff00')
                self.ids.display_correct.color = hex('#00FF00')
                self.ids.display_correct.text = "Correct!"
                GameOneScreen.correct += 1

                if int(self.ids.counter.text) >= (time_per_round - round(MainMenu.difficulty_coefficient * 2)):
                    GameOneScreen.score += (25 * MainMenu.difficulty_coefficient)
                elif int(self.ids.counter.text) >= (time_per_round - round(MainMenu.difficulty_coefficient * 5)):
                    GameOneScreen.score += 20 * MainMenu.difficulty_coefficient
                else:
                    GameOneScreen.score += 10 * MainMenu.difficulty_coefficient

                self.generate_question()
                GameOneScreen.answered = not GameOneScreen.answered
            else:
                button_id.color = hex('#ff0000')
                GameOneScreen.incorrect += 1
                GameOneScreen.score -= 5

    def generate_question(self):
        GameOneScreen.current_round_number += 1

        if GameOneScreen.current_round_number != 1:
            Clock.schedule_once(self.add_to_clock, 3)
            Clock.schedule_once(self.generate_question_complement, 3)
            self.remove_from_clock()
        else:
            self.generate_question_complement(None)

    def generate_question_complement(self, dt):
        buttons_list = [self.ids.answer_one, self.ids.answer_two, self.ids.answer_three, self.ids.answer_four,
                        self.ids.answer_five, self.ids.answer_six]

        GameOneScreen.answered = False
        self.reset_buttons()
        if GameOneScreen.current_round_number != round_number + 1:
            GameOneScreen.factor_one = str(self.random_number())
            GameOneScreen.factor_two = str(random.sample(decimal_numbers, 1)[0])
            self.ids.game_one_question.text = f"{GameOneScreen.factor_one} × {GameOneScreen.factor_two} = ?"

            correct_answer = int(GameOneScreen.factor_one) * int(GameOneScreen.factor_two)

            correct_button = random.sample(buttons_list, 1)[0]
            correct_button.text = str(correct_answer)

            buttons_list.remove(correct_button)

            available_choices = [str(correct_answer)]

            for button in buttons_list:
                button.text = str(random.randint(round(0.4 * correct_answer), round(2 * correct_answer)))
                try:
                    self.ids.game_one_question.font_size = 5 * int(SettingsPage.font_size.replace("px", "")) + random.randint(-10, 10)
                except:
                    pass
                try:
                    button.font_size = SettingsPage.font_size + random.randint(-3, 5)
                except:
                    pass
                while button.text in available_choices:
                    if correct_answer > 10:
                        button.text = str(random.randint(round(0.4 * correct_answer), round(2 * correct_answer)))
                    else:
                        button.text = str(random.randint(1, 11))
                available_choices.append(button.text)
        else:
            self.manager.current = "score_screen_one"

    def reset_buttons(self):
        buttons_list = [self.ids.answer_one, self.ids.answer_two, self.ids.answer_three, self.ids.answer_four,
                        self.ids.answer_five, self.ids.answer_six]

        GameOneScreen.answered = False
        for button in buttons_list:
            button.text = ""
            button.color = hex('#000000')
        self.ids.display_correct.text = ""
        self.ids.counter.text = str(time_per_round)

    def random_number(self):
        return int(random.sample(selected_numbers_list, 1)[0])

class GameTwoScreen(Screen):
    counter = None

    current_round_number = 0

    correct = 0
    incorrect = 0
    score = 0

    answered = False

    factor_one = 0
    factor_two = 0

    answer = 0

    input_number = ""

    def on_pre_enter(self, *args):
        GameTwoScreen.current_round_number = 0

        GameTwoScreen.correct = 0
        GameTwoScreen.incorrect = 0
        GameTwoScreen.score = 0

        self.generate_question()
        self.reset_buttons(None)
        self.add_to_clock(None)

    def add_to_clock(self, dt):
        GameTwoScreen.counter = Clock.schedule_interval(self.decrease_counter, 1)

    def remove_from_clock(self):
        GameTwoScreen.counter.cancel()

    def decrease_counter(self, dt):
        if int(self.ids.counter.text) != 0:
            self.ids.counter.text = str(int(self.ids.counter.text) - 1)
        else:
            self.ids.display_correct.color = hex('#FF0000')
            self.ids.display_correct.text = "TIME OUT!"
            self.generate_question()
            GameTwoScreen.answered = True
            GameTwoScreen.score -= 10

    def generate_question(self):
        GameTwoScreen.current_round_number += 1

        if GameTwoScreen.current_round_number != 1:
            Clock.schedule_once(self.add_to_clock, 3)
            Clock.schedule_once(self.generate_question_complement, 3)
            self.remove_from_clock()
        else:
            self.generate_question_complement(None)

    def generate_question_complement(self, dt):
        GameTwoScreen.answered = False

        self.reset_buttons(None)

        if GameTwoScreen.current_round_number != round_number + 1:
            GameTwoScreen.factor_one = self.random_number()
            GameTwoScreen.factor_two = random.sample(decimal_numbers, 1)[0]

            GameTwoScreen.answer = GameTwoScreen.factor_one * GameTwoScreen.factor_two

            GameTwoScreen.input_number = "?"

            self.ids.game_two_question.text = f"{str(GameTwoScreen.factor_one)} × {GameTwoScreen.factor_two} = {GameTwoScreen.input_number}"
            try:
                self.ids.game_two_question.font_size = 5 * int(SettingsPage.font_size.replace("px", "")) + random.randint(-10, 10)
            except:
                pass
        else:
            self.manager.current = "score_screen_two"

    def input(self, number):

        GameTwoScreen.input_number = GameTwoScreen.input_number.replace("?", "") + str(number)

        self.ids.game_two_question.text = f"{str(GameTwoScreen.factor_one)} × {GameTwoScreen.factor_two} = {GameTwoScreen.input_number}"

    def reset_buttons(self, dt):
        self.ids.counter.text = str(time_per_round)
        self.ids.display_correct.text = ""
        GameTwoScreen.input_number = "?"

    def backspace(self):
        GameTwoScreen.input_number = str(GameTwoScreen.input_number).replace("?", "")[0:len(GameTwoScreen.input_number) - 1]

        if len(GameTwoScreen.input_number) == 0:
            GameTwoScreen.input_number = "?"

        self.ids.game_two_question.text = f"{str(GameTwoScreen.factor_one)} × {GameTwoScreen.factor_two} = {GameTwoScreen.input_number}"

    def submit(self):
        if GameTwoScreen.input_number == str(GameTwoScreen.answer) and GameTwoScreen.answered == False:
            GameTwoScreen.answered = True

            self.ids.display_correct.color = hex('#00FF00')
            self.ids.display_correct.text = "Correct!"
            self.generate_question()

            GameTwoScreen.correct += 1

            if int(self.ids.counter.text) >= (time_per_round - round(MainMenu.difficulty_coefficient * 3)):
                GameTwoScreen.score += 25
            elif int(self.ids.counter.text) >= (time_per_round - round(MainMenu.difficulty_coefficient * 6)):
                GameTwoScreen.score += 20
            else:
                GameTwoScreen.score += 10

        elif not GameTwoScreen.answered:
            self.ids.display_correct.color = hex('#FF0000')
            self.ids.display_correct.text = "WRONG!"
            Clock.schedule_once(self.remove_wrong, 1)

            if SettingsPage.delete_after_wrong:
                GameTwoScreen.input_number = "?"
                self.ids.game_two_question.text = f"{str(GameTwoScreen.factor_one)} × {GameTwoScreen.factor_two} = {GameTwoScreen.input_number}"

            GameTwoScreen.score -= 5
        else:
            pass

    def return_to_main(self):
        GameTwoScreen.answered = False
        self.reset_buttons(None)
        self.manager.current = "main_menu"
        self.remove_from_clock()

    def remove_wrong(self, dt):
        if self.ids.display_correct.text == "WRONG!":
            self.ids.display_correct.text = ""

    def random_number(self):
        return int(random.sample(selected_numbers_list, 1)[0])

class GameThreeScreen(Screen):
    counter = None

    current_round_number = 0

    correct = 0
    incorrect = 0
    score = 0

    answered = False

    factor_one = 0
    factor_two = 0

    correct_answer = 0

    def on_pre_enter(self, *args):

        GameThreeScreen.current_round_number = 0
        GameThreeScreen.correct = 0
        GameThreeScreen.incorrect = 0
        GameThreeScreen.score = 0

        self.ids.counter.text = str(time_per_round)
        self.add_to_clock(None)
        self.generate_question()

    def add_to_clock(self, dt):
        if self.manager.current == "game_three":
            GameThreeScreen.counter = Clock.schedule_interval(self.decrease_counter, 1)

    def remove_from_clock(self):
        if self.manager.current == "game_three":
            GameThreeScreen.counter.cancel()

    def decrease_counter(self, dt):

        if int(self.ids.counter.text) != 0:
            self.ids.counter.text = str(int(self.ids.counter.text) - 1)
        else:
            self.ids.display_correct.color = hex('#FF0000')
            self.ids.display_correct.text = "TIME OUT!"
            self.generate_question()
            GameThreeScreen.answered = True

            GameThreeScreen.incorrect += 1
            GameThreeScreen.score -= 20

    def return_to_main(self):
        GameThreeScreen.answered = False
        self.reset_buttons()
        self.remove_from_clock()
        self.manager.current = "main_menu"

    def answer(self, button_id):
        if not GameThreeScreen.answered:
            if int(button_id.text) == int(GameThreeScreen.factor_two):
                button_id.color = hex('#48ff00')
                self.ids.display_correct.color = hex('#00FF00')
                self.ids.display_correct.text = "Correct!"
                GameThreeScreen.correct += 1

                if int(self.ids.counter.text) >= (time_per_round - round(MainMenu.difficulty_coefficient * 2)):
                    GameThreeScreen.score += 25 * MainMenu.difficulty_coefficient
                elif int(self.ids.counter.text) >= (time_per_round - round(MainMenu.difficulty_coefficient * 5)):
                    GameThreeScreen.score += 20 * MainMenu.difficulty_coefficient
                else:
                    GameThreeScreen.score += 10 * MainMenu.difficulty_coefficient

                self.generate_question()
                GameThreeScreen.answered = not GameThreeScreen.answered
            else:
                button_id.color = hex('#ff0000')
                GameThreeScreen.incorrect += 1
                GameThreeScreen.score -= 5

    def generate_question(self):
        GameThreeScreen.current_round_number += 1

        if GameThreeScreen.current_round_number != 1:
            Clock.schedule_once(self.add_to_clock, 3)
            Clock.schedule_once(self.generate_question_complement, 3)
            self.remove_from_clock()
        else:
            self.generate_question_complement(None)

    def generate_question_complement(self, dt):
        buttons_list = [self.ids.answer_one, self.ids.answer_two, self.ids.answer_three, self.ids.answer_four,
                        self.ids.answer_five, self.ids.answer_six]

        GameThreeScreen.answered = False
        self.reset_buttons()
        if GameThreeScreen.current_round_number != round_number + 1:
            GameThreeScreen.factor_one = str(self.random_number())
            GameThreeScreen.factor_two = str(random.sample(decimal_numbers, 1)[0])

            GameThreeScreen.correct_answer = int(GameThreeScreen.factor_one) * int(GameThreeScreen.factor_two)

            self.ids.game_one_question.text = f"{GameThreeScreen.factor_one} × ? = {GameThreeScreen.correct_answer}"
            try:
                self.ids.game_one_question.font_size = 5 * int(SettingsPage.font_size.replace("px", "")) + random.randint(-10, 10)
            except:
                pass
            correct_button = random.sample(buttons_list, 1)[0]
            correct_button.text = str(GameThreeScreen.factor_two)

            buttons_list.remove(correct_button)

            available_choices = [str(GameThreeScreen.factor_two)]

            for button in buttons_list:
                button.text = str((random.sample(decimal_numbers, 1)[0]))
                try:
                    button.font_size = SettingsPage.font_size + random.randint(-3, 5)
                except:
                    pass
                while button.text in available_choices:
                    button.text = str((random.sample(decimal_numbers, 1)[0]))
                available_choices.append(button.text)
        else:
            self.manager.current = "score_screen_three"

    def reset_buttons(self):
        buttons_list = [self.ids.answer_one, self.ids.answer_two, self.ids.answer_three, self.ids.answer_four,
                        self.ids.answer_five, self.ids.answer_six]

        GameThreeScreen.answered = False
        for button in buttons_list:
            button.text = ""
            button.color = hex('#000000')
        self.ids.display_correct.text = ""
        self.ids.counter.text = str(time_per_round)

    def random_number(self):
        return int(random.sample(selected_numbers_list, 1)[0])


class ScoreScreenOne(Screen):
    def on_pre_enter(self, *args):
        self.ids.raw_score.text = f"{GameOneScreen.correct}/{round_number}"
        self.ids.score.text = f"Total Score: {round(GameOneScreen.score)}"

    def return_to_main(self):
        self.manager.current = "main_menu"


class ScoreScreenTwo(ScoreScreenOne):
    def on_pre_enter(self, *args):
        self.ids.raw_score.text = f"{GameTwoScreen.correct}/{round_number}"
        self.ids.score.text = f"Total Score: {round(GameTwoScreen.score)}"

class ScoreScreenThree(ScoreScreenOne):
    def on_pre_enter(self, *args):
        self.ids.raw_score.text = f"{GameThreeScreen.correct}/{round_number}"
        self.ids.score.text = f"Total Score: {round(GameThreeScreen.score)}"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    font_size = StringProperty(SettingsPage.font_size)
    button_color = ListProperty(SettingsPage.button_color)
    roundness = StringProperty(SettingsPage.roundness)
    delete_option_text = StringProperty(SettingsPage.delete_option_text)

    def build(self):
        return RootWidget()

class ColorButton(Button):
    pass


if __name__ == "__main__":
    MainApp().run()