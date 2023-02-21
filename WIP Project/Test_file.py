from matplotlib import pyplot as mplot
"""
x = [t/10 for t in range(0, 100)]
y = [t**3 for t in x]

fig, ax = mplot.subplots()
ax.plot(x, y, label = "$y=x^3$")
mplot.savefig(f'Plot/plot.png')
"""

x = [t/10 for t in range(0, 100)]
y = [t**2 for t in x]

fig, ax = mplot.subplots()
ax.plot(x, y, label = "$y=x^2$")
ax.legend()
ax.set_title("$y=x^2$")
mplot.savefig(f'Plot/plot.png')
