def missing_boi():
    n = input()
    nums = input()
    nums += " "
    numbers_list = [0]
    number = ""
    for char in nums:
        if char != " ":
            number += char
        elif char == " ":
            numbers_list.append(int(number))
            number = ""

    numbers_list.sort()
    numbers_list.append(0)
    for i in range(1, len(numbers_list)):
        if numbers_list[i] != i:
            print(i)
            break


missing_boi()