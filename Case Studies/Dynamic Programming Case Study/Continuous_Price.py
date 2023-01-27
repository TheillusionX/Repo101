"""
IE361 Case Study - Group 12
Abderrahmane Harkat     2415297
Alperen Oktay Şahin     2305373
Youssef Nsouli          2487494

Author: Youssef Nsouli
"""
from functools import cache
from math import factorial
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, MultipleLocator

start_time = 144
max_seating = 90
max_overbooking = 10
no_show_up_rate = 0.05
penalty_rate = 200
b = 710
a = 41

@cache
def customer_arrival_rate(t):
    return 0.9

@cache
def combination(n, r):
    return factorial(n)/(factorial(r)*factorial(n - r))


optimal_prices = pd.DataFrame(columns = ["t: 1"])


@cache
def penalty(s):
    if s > max_seating:
        summation = 0
        for i in range(max_seating, s):
            summation += combination(s, i) * pow(1 - no_show_up_rate, i) * pow(no_show_up_rate, s - i) * (i - max_seating) * penalty_rate
        return summation
    else:
        return 0

@cache
def revenue(t, s):
    if t == 0:
        return 0 - penalty(s)
    elif s > max_seating + max_overbooking:
        # optimal_prices.loc[f"Seats: {s}", f"t: {t}"] = f"None"
        return 0 + revenue(t - 1, s)

    else:
        crt = customer_arrival_rate(t)
        x = (1 / 2) * (b - revenue(t - 1, s + 1) + revenue(t - 1, s))

        if x < a:
            price = a
        elif x > b:
            price = b
        else:
            price = x

        p = (price - a)/(b - a)

        optimal_prices.loc[f"Seats: {s}", f"t: {t}"] = float(f"{price:.2f}")

        return crt*((1 - p)*(price + revenue(t - 1, s + 1)) + p*revenue(t - 1, s)) + (1 - crt)*(revenue(t - 1, s))

print(revenue(start_time, 0))
# optimal_prices.to_excel("Optimal_Prices_Continuous.xlsx")
# optimal_prices.to_csv("Optimal_Prices_Continuous.csv")

fig, (ax1, ax2) = plt.subplots(ncols = 2)
ax1.plot(range(1, 145), optimal_prices.loc["Seats: 95"], color = "red")
ax2.plot(range(1, 145), optimal_prices.loc["Seats: 70"], color = "blue")
fig.suptitle("Optimal Prices for Certain Seat Inventory Levels, s")

ax1.set_title(r"$s = 95$")
ax1.set_xlabel(r"Time until Flight, $t$")
ax1.set_ylabel(r"Optimal Prices, $x_{ts}$, in \$")
ax1.spines["top"].set_color("None")
ax1.spines["left"].set_color("None")
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()
ax1.set_xlim([0, start_time + 1])
ax1.set_ylim([0, b + 100])
ax1.axvline(x = 49, ymax = b/(b + 50), ls = "--", lw = 1, color = "gray", alpha = 0.5)
ax1.xaxis.set_minor_locator(FixedLocator([49, start_time]))
ax1.xaxis.set_minor_formatter(FixedFormatter([49, r"$T$"]))
ax1.xaxis.set_major_locator(MultipleLocator(30))
ax1.tick_params(axis = "x", which = "minor", direction = "out", length = 10, width = 1)
ax1.scatter((49, 1), (optimal_prices.loc["Seats: 95", "t: 49"], optimal_prices.loc["Seats: 95", "t: 1"]), color = "red")
ax1.annotate("${0}".format(optimal_prices.loc["Seats: 95", "t: 49"]), (49, optimal_prices.loc["Seats: 95", "t: 49"]), xytext = (-25, 2), textcoords = "offset points", fontsize = "xx-small", alpha = 0.8)
ax1.annotate("${0}".format(optimal_prices.loc["Seats: 95", "t: 1"]), (1, optimal_prices.loc["Seats: 95", "t: 1"]), xytext = (-25, -8), textcoords = "offset points", fontsize = "xx-small", alpha = 0.8)
ax1.fill_between(x = [0, start_time + 1], y1 = [b] * 2, y2 = [a] * 2, color = "gray", alpha = 0.1)
ax1.text(start_time - 3, a + 10, "Feasible Price Region", fontsize = "x-small", style = "italic", alpha = 0.5)

ax2.set_title(r"$s = 70$")
ax2.set_xlabel(r"Time until Flight, $t$")
ax2.spines["top"].set_color("None")
ax2.spines["left"].set_color("None")
ax2.yaxis.tick_right()
ax2.set_xlim([0, start_time + 1])
ax2.set_ylim([0, b + 100])
ax2.axvline(x = 74, ymax = b/(b + 50), ls = "--", lw = 1, color = "gray", alpha = 0.5)
ax2.xaxis.set_minor_locator(FixedLocator([74, start_time]))
ax2.xaxis.set_minor_formatter(FixedFormatter([74, r"$T$"]))
ax2.xaxis.set_major_locator(MultipleLocator(30))
ax2.tick_params(axis = "x", which = "minor", direction = "out", length = 10, width = 1)
ax2.scatter(74, optimal_prices.loc["Seats: 70", "t: 74"], color = "blue")
ax2.annotate("${0}".format(optimal_prices.loc["Seats: 70", "t: 74"]), (74, optimal_prices.loc["Seats: 70", "t: 74"]), xytext = (-27, 2), textcoords = "offset points", fontsize = "xx-small", alpha = 0.8)
ax2.axhline(y = optimal_prices.loc["Seats: 70", "t: 1"], xmin = 1 - 100/start_time, color = "gray", ls = "--", lw = 1, alpha = 0.5)
ax2.text(start_time - 5, optimal_prices.loc["Seats: 70", "t: 1"], r"$x_{t,70}= \$355$", va = "center_baseline", fontsize = "x-small", alpha = 0.8)
ax2.fill_between(x = [0, start_time + 1], y1 = [b] * 2, y2 = [a] * 2, color = "gray", alpha = 0.1)
ax2.text(start_time - 3, a + 10, "Feasible Price Region", fontsize = "x-small", style = "italic", alpha = 0.5)

ax1.invert_xaxis()
ax2.invert_xaxis()
fig.tight_layout()
plt.show()

fig, (ax1, ax2) = plt.subplots(ncols = 2)
ax1.plot(range(0, max_seating + max_overbooking + 1), optimal_prices.loc[:, "t: 1"][::-1], color = "red")
ax2.plot(range(0, max_seating + max_overbooking + 1), optimal_prices.loc[:, "t: 20"][::-1], color = "blue")
fig.suptitle("Optimal Prices at Certain Time Stages, t")

ax1.set_title(r"$t = 1$")
ax1.set_xlabel(r"Number of Seats, $s$")
ax1.set_ylabel(r"Optimal Prices, $x_{ts}$, in \$")
ax1.spines["top"].set_color("None")
ax1.spines["right"].set_color("None")
ax1.set_xlim([0, max_seating + max_overbooking])
ax1.set_ylim([0, b + 100])
ax1.scatter(100, optimal_prices.iloc[0, 0], color = "red")
ax1.annotate(fr"$\${optimal_prices.iloc[0,0]}$", (100, optimal_prices.iloc[0, 0]), xytext = (-15, 10), textcoords = "offset points", fontsize = "xx-small", alpha = 0.8)
ax1.axvline(x = max_seating, ymax = b/(b + 50), ls = "--", lw = 1, color = "gray", alpha = 0.5)
ax1.xaxis.set_minor_locator(FixedLocator([max_seating]))
ax1.xaxis.set_minor_formatter(FixedFormatter([rf"$S={max_seating}$"]))
ax1.tick_params(axis = "x", which = "minor", direction = "out", length = 14, width = 1, labelsize = 8)
ax1.yaxis.set_minor_locator(FixedLocator([355]))
ax1.yaxis.set_minor_formatter(FixedFormatter(["355"]))
ax1.tick_params(axis = "y", which = "minor", direction = "out", length = 3, width = 1, labelsize = 6)
ax1.axhline(y = 355, color = "gray", ls = "--", lw = 1, alpha = 0.5)
ax1.fill_between(x = [0, start_time + 1], y1 = [b] * 2, y2 = [a] * 2, color = "gray", alpha = 0.1)
ax1.text(5, a + 10, "Feasible Price Region", fontsize = "x-small", style = "italic", alpha = 0.5)

ax2.set_title(r"$t = 20$")
ax2.set_xlabel(r"Number of Seats, $s$")
ax2.spines["top"].set_color("None")
ax2.spines["right"].set_color("None")
ax2.set_xlim([0, max_seating + max_overbooking])
ax2.set_ylim([0, b + 100])
ax2.scatter(100, optimal_prices.iloc[0, 19], color = "blue")
ax2.annotate(fr"$\${optimal_prices.iloc[0,19]}$", (100, optimal_prices.iloc[0, 19]), xytext = (-15, 10), textcoords = "offset points", fontsize = "xx-small", alpha = 0.8)
ax2.axvline(x = max_seating, ymax = b/(b + 50), ls = "--", lw = 1, color = "gray", alpha = 0.5)
ax2.xaxis.set_minor_locator(FixedLocator([max_seating]))
ax2.xaxis.set_minor_formatter(FixedFormatter([rf"$S={max_seating}$"]))
ax2.tick_params(axis = "x", which = "minor", direction = "out", length = 14, width = 1, labelsize = 8)
ax2.yaxis.set_minor_locator(FixedLocator([355]))
ax2.yaxis.set_minor_formatter(FixedFormatter(["355"]))
ax2.tick_params(axis = "y", which = "minor", direction = "out", length = 3, width = 1, labelsize = 6)
ax2.axhline(y = 355, color = "gray", ls = "--", lw = 1, alpha = 0.5)
ax2.fill_between(x = [0, start_time + 1], y1 = [b] * 2, y2 = [a] * 2, color = "gray", alpha = 0.1)
ax2.text(5, a + 10, "Feasible Price Region", fontsize = "x-small", style = "italic", alpha = 0.5)

fig.tight_layout()

plt.show()
