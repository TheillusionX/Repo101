from random import *


def bin_search(list1, x):
    print(list1, "")

    if len(list1) > 1:
        median = round(len(list1)/2) - 1
        if x == list1[median]:
            return True

        elif x > list1[median]:
            temp = list1[median + 1:]
            list1 = temp
            bin_search(temp, x)

        elif x < list1[median]:
            temp = list1[0:median]
            list1 = temp
            bin_search(temp, x)

    if x in list1:
        return True
    else:
        return False


lst = []
i = 0
while len(lst) < 1001:
    n = i + randint(0, 5)
    lst.append(n)
    i = n

x = randint(0, lst[-1])
print(bin_search(lst, x))
#print(list1)