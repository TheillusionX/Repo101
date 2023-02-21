from tkinter import *
import pandas
from difflib import SequenceMatcher

def sim(a, b):
    return SequenceMatcher(None, a, b).ratio()


window = Tk()

scroll = Scrollbar(window)
scroll.grid(row = 2, column = 2, rowspan = 7)
#
listbox = Listbox(window, yscrollcommand = scroll, width = 50)
listbox.grid(row = 2, column = 0, rowspan = 7, columnspan = 3)
#
scroll.config(command = listbox.yview)

data = pandas.DataFrame(columns = ["Title", "Year", "Author", "ISBN"])
data = data.T

data["0"] = ["In The Sun", "2019", "Rowling", "6619"]
data["1"] = ["Maze Runner", "2002", "James", "909090"]
data["2"] = ["The Booth", "1990", "Emily", "8989"]
data["3"] = ["Maze Runner 2", "2004", "James", "8871"]

data = data.T

Title = list(data["Title"])
Year = list(data["Year"])
Author = list(data["Author"])
ISBN = list(data["ISBN"])

title_entry_value = StringVar()
title_entry = Entry(window, textvariable = title_entry_value)
title_entry.grid(row = 0, column = 1)

year_entry_value = StringVar()
year_entry = Entry(window, textvariable = year_entry_value)
year_entry.grid(row = 1, column = 1)

author_entry_value = StringVar()
author_entry = Entry(window, textvariable = author_entry_value)
author_entry.grid(row = 0, column = 3)

isbn_entry_value = StringVar()
isbn_entry = Entry(window, textvariable = isbn_entry_value)
isbn_entry.grid(row = 1, column = 3)

def view_all():
    listbox.delete(0, END)
    for title, year, author, isbn in zip(Title, Year, Author, ISBN):
        listbox.insert(ACTIVE, f"{title}, {year}, {author}, {isbn}")

def search():
    i = 0
    listbox.delete(0, END)
    search_term = title_entry_value.get()

    for title, year, author, isbn in zip(Title, Year, Author, ISBN):
        if sim(search_term.lower(), str(title[0:len(search_term)]).lower()) > 0.8:
            listbox.insert(ACTIVE, f"{title}, {year}, {author}, {isbn}")
            i += 1
    if i == 0:
        listbox.insert(ACTIVE, "No results")

def add():
    global data
    new_title = str(title_entry_value.get())
    new_year = str(year_entry_value.get())
    new_author = str(author_entry_value.get())
    new_isbn = str(isbn_entry_value.get())

    tempodata = pandas.DataFrame([[new_title, new_year, new_author, new_isbn]], columns = ["Title", "Year", "Author", "ISBN"])
    data = data.append(tempodata, ignore_index = True, verify_integrity = True)

    Title.append(new_title)
    Year.append(new_year)
    Author.append(new_author)
    ISBN.append(new_isbn)
    view_all()

def update():
    global data, Title, Year, Author, ISBN
    new_title = str(title_entry_value.get())
    new_year = str(year_entry_value.get())
    new_author = str(author_entry_value.get())
    new_isbn = str(isbn_entry_value.get())

    old_entry = str(listbox.get(ACTIVE))
    if len(old_entry) != 0:
        i = 0
        old_title = ""

        for char in old_entry:
            if char == ",":
                break
            else:
                old_title = old_title + char

        tempodata = data.set_index("Title").T
        tempodata[old_title] = [new_year, new_author, new_isbn]
        tempodata.rename(columns = {old_title : new_title}, inplace=True)
        data = tempodata.T.reset_index(drop = False)

        Title = list(data["Title"])
        Year = list(data["Year"])
        Author = list(data["Author"])
        ISBN = list(data["ISBN"])
        view_all()


def delete_entry():
    global data, Title, Year, Author, ISBN
    new_title = str(title_entry_value.get())

    old_entry = str(listbox.get(ACTIVE))
    if len(old_entry) != 0:
        i = 0
        old_title = ""

        for char in old_entry:
            if char == ",":
                break
            else:
                old_title = old_title + char

        tempodata = data.set_index("Title").T
        del tempodata[old_title]
        data = tempodata.T.reset_index(drop = False)

        Title = list(data["Title"])
        Year = list(data["Year"])
        Author = list(data["Author"])
        ISBN = list(data["ISBN"])
        view_all()


title_label = Label(window, text = "Title")
title_label.grid(row = 0, column = 0)

year_label = Label(window, text = "Year")
year_label.grid(row = 1, column = 0)

author_label = Label(window, text = "Author")
author_label.grid(row = 0, column = 2)

isbn_label = Label(window, text = "ISBN")
isbn_label.grid(row = 1, column = 2)

ViewAll_button = Button(window, text = "View All", width = 10, command = view_all)
ViewAll_button.grid(row = 2, column = 3)

Search_button = Button(window, text = "Search Entry", width = 10, command = search)
Search_button.grid(row = 3, column = 3)

Add_button = Button(window, text = "Add Entry", width = 10, command = add)
Add_button.grid(row = 4, column = 3)

Update_button = Button(window, text = "Update", width = 10, command = update)
Update_button.grid(row = 5, column = 3)

Delete_button = Button(window, text = "Delete Entry", width = 10, command = delete_entry)
Delete_button.grid(row = 6, column = 3)

Close_button = Button(window, text = "Close", width = 10, command = window.destroy)
Close_button.grid(row = 7, column = 3)

window = mainloop()