from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty
import pandas
from datetime import datetime
from csv import writer

employees = pandas.read_csv("Employees.csv")
branches = pandas.read_csv("Branches.csv")

temp_scale = [str(x/10) for x in range(350, 405, 5)]
temp_scale.insert(0, "Low")
temp_scale.insert(len(temp_scale), "High")

branches["Branch ID"] = [str(x) for x in list(branches["Branch ID"])]

Builder.load_file("frontend.kv")

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def branch_select(self, text):
        selected_id = text
        selected_id_index = list(branches["Branch ID"]).index(selected_id)
        self.ids.branch_info.text = f"{list(branches['Branch Name'])[selected_id_index]} - ID: {selected_id}"

    def employee_select(self, emp_id):
        try:
            employee_id = int(emp_id)
            if employee_id in list(employees["Employee ID"]):
                emp_id_index = list(employees["Employee ID"]).index(employee_id)
                fn = list(employees["Employee First Name"])[emp_id_index]
                ln = list(employees["Employee Last Name"])[emp_id_index]
                self.ids.employee_info.color = [1, 1, 1, 1]
                self.ids.employee_info.italic = False
                self.ids.employee_info.text = f"{fn} {ln}"
        except:
            self.ids.employee_info.text = "Enter a valid ID"
            self.ids.employee_info.color = [1, 0, 0, 1]
            self.ids.employee_info.italic = True
        #print(list(employees["Employee ID"])[0])

    def temp_color(self, new_text):
        if new_text == "High":
            self.ids.temp.color = [1, 0, 0, 1]
            self.ids.temp.text = new_text
        elif new_text == "Low":
            self.ids.temp.color = [0, 0, 1, 1]
        else:
            self.ids.temp.color = [0, 0, 0, 1]
        self.ids.temp.text = new_text

    def temp_up(self, temp):
        index = temp_scale.index(temp)
        try:
            new_text = temp_scale[index + 1]
            self.temp_color(new_text)
        except:
            pass

    def temp_down(self, temp):
        index = temp_scale.index(temp)
        if self.ids.temp.text != "Low":
            new_text = temp_scale[index - 1]
            self.temp_color(new_text)
        else:
            pass

    def submit(self, emp_id, branch_id, temp):
        if len(emp_id) > 0 and branch_id != "Enter Branch ID":
            current_time = datetime.now()
            with open("temperatures.csv", 'a+', newline='') as write_obj:
                csv_writer = writer(write_obj)
                csv_writer.writerow([emp_id, branch_id, temp, current_time])
            self.ids.success_or_error.color = [1, 1, 1, 1]
            self.ids.success_or_error.text = "Upload Success"
        else:
            self.ids.success_or_error.color = [1, 0, 0, 1]
            self.ids.success_or_error.text = "Please Enter an employee ID and a branch ID"


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    branch_ids = ListProperty(list(branches["Branch ID"]))

    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()