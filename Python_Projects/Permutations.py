from secrets import choice

def permuting_boi(n):
    beautiful_permutation = []
    beautiful = False

    n_range = [None] + list(range(1, n + 1))
    count = 0
    while not beautiful:
        count += 1
        if count > n ** n:
            return "NO SOLUTION"
        beautiful_permutation = []
        beautiful = True
        x_range = n_range[1:]
        for _ in range(1, n + 1):
            x = choice(x_range)
            beautiful_permutation.append(str(x))
            x_range.remove(x)

        for i in range(1, len(beautiful_permutation)):
            if abs(int(beautiful_permutation[i]) - int(beautiful_permutation[i - 1])) == 1:
                beautiful = False
                break


    return " ".join(beautiful_permutation)


print(permuting_boi(int(input())))