import matplotlib.pyplot as mplot
from datetime import datetime as date

def plot(x, y, title, file_name, plt_type = "Linear", overwrite = True):
    if plt_type == "Linear":
        fig, ax = mplot.subplots()
        ax.plot(x, y, label = title)
        ax.legend()
        ax.set_title(title)

        if overwrite: mplot.savefig(f'Plot/{file_name}.png')
        else: mplot.savefig(f'Plot/{file_name}{date.now().strftime("%d%m%y%H%M%S")}.png')
    elif plt_type == "Histo":
        pass
