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

start_time = 144
max_seating = 90
max_overbooking = 10
no_show_up_rate = 0.05
penalty_rate = 200


def customer_arrival_rate(t):
    return 0.9


# Calculates the CDF of a probability for a value x
@cache
def probability(x, t, a=41, b=710):
    return (x - a)/(b - a)
    #return pow(x/b, 2)
    #return 0.1 * pow(x/b, 2) + 0.9 * pow((start_time - t) / start_time, 2)


@cache
def combination(n, r):
    return factorial(n)/(factorial(r)*factorial(n - r))


@cache
def penalty(s):
    if s > max_seating:
        summation = 0
        for i in range(max_seating, s):
            summation += combination(s, i) * pow(1 - no_show_up_rate, i) * pow(no_show_up_rate, s - i) * (i - max_seating) * penalty_rate
        return summation
    else:
        return 0


optimal_prices = pd.DataFrame(columns = ["t: 1"])


@cache
def revenue(t, s):
    if t == 0:
        return 0 - penalty(s)
    elif s > max_seating + max_overbooking:
        return 0 + revenue(t - 1, s)
    else:
        x = 0
        vals_dict = {}
        crt = customer_arrival_rate(t)

        while probability(x, t) <= 1:
            p = probability(x, t)
            val = crt*((1 - p)*(x + revenue(t - 1, s + 1)) + p*revenue(t - 1, s)) + (1 - crt)*(revenue(t - 1, s))
            if p >= 0:
                vals_dict[x] = val
            x += 1

        mx = max(vals_dict.values())
        x = max(vals_dict, key=vals_dict.get)
        optimal_prices.loc[f"Seats: {s}", f"t: {t}"] = float(f"{x:.2f}")
        return mx


print(revenue(start_time, 0))
# print(probability(710, 144))
optimal_prices.to_excel("Optimal_Prices_Discrete.xlsx")
