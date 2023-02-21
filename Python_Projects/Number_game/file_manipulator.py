import json
dct = {"font_size" : "12px",
       "button_color" : ['#fffb00', '#949200'],
       "roundness" : "10",
       "delete_after_wrong" : False,
       "difficulty" : "easy",
       "easy" : "All factors range from 1 to 10",
       "medium" : "The second factor ranges from 1 to 20",
       "hard" : "The second factor range from 1 to 20. The first factor can be chosen amongst numbers between 10 and 19"}

with open("preferences.txt", "r+") as file:
    json.dump(dct, file, indent = 1)