def login_success(users, username, password):
    for user in users:
        if user == username and password == users[user]:
            return True
    return False


def convert_to_morse(input_string, morse_dict):
    morse_code = ""

    for char in input_string:
        morse_code += morse_dict[char.upper()]
        morse_code += " "
    return morse_code


def code_reversal(dct):
    new_dict = {}
    for old_key in dct:
        old_value = dct[old_key]
        new_dict[old_value] = old_key
    return new_dict


def convert_from_morse(input_morse, morse_dict):
    morse_letter = ""
    morse_list = []
    input_morse += " "
    output = ""

    for key in morse_dict:
        morse_list.append(key)

    for char in input_morse:
        morse_letter = morse_letter + char
        if morse_letter.replace(" ", "") in morse_list and char == " ":
            output = output + morse_dict[morse_letter.replace(" ", "")]
            morse_letter = ""

    return output


def parentheses_and_braces_checker(s):
    parentheses1 = ["(", "["]
    parentheses2 = [")", "]"]
    tempo = ""

    for char in s:
        if char in parentheses1 or char in parentheses2:
            tempo += char

            if tempo[0:round(len(tempo)/2)][::-1] == tempo[round(len(tempo)/2):].replace(")", "(").replace("]", "[") and char in parentheses2:
                tempo = ""

    if tempo == "":
        return True
    else:
        return False


def anagrams(s1, s2):
    letter_dict1 = {}
    letter_dict2 = {}
    for char in s1:
        if char not in letter_dict1.keys():
            letter_dict1[char] = 1
        else:
            letter_dict1[char] += 1

    for char in s2:
        if char not in letter_dict2.keys():
            letter_dict2[char] = 1
        else:
            letter_dict2[char] += 1

    if letter_dict1 == letter_dict2:
        return True
    else:
        return False


def display_mean():
    input_num = ""
    pos_nums = []
    neg_nums = []
    while True:
        input_num = input("Enter a new data point: ")

        if input_num == "*":
            break
        else:
            input_num = int(input_num)

        if input_num >= 0:
            pos_nums.append(input_num)
        elif input_num < 0:
            neg_nums.append(input_num)
        else:
            pass

        print(f"* Number of positive values: {len(pos_nums)}")
        print(f"* Sum of positive values: {sum(pos_nums)}")
        print(f"* Average of positive values: {sum(pos_nums)/len(pos_nums) if len(pos_nums) != 0 else 0}")

        print(f"* Number of negative values: {len(neg_nums)}")
        print(f"* Sum of negative values: {sum(neg_nums)}")
        print(f"* Average of negative values: {sum(neg_nums) / len(neg_nums) if len(neg_nums) != 0 else 0}\n")


def pmf():
    ele = ""
    pmf_list = []
    pmf = input("Enter PMF: ")
    unimodal = True

    pmf += " "
    i = -1
    for char in pmf:
        i += 1
        if char != " ":
            ele += char
        else:
            pmf_list.append(float(ele))
            ele = ""

    if sum(pmf_list) != 1:
        print("This set is not a viable PMF")
        return None

    summ = 0.0
    prev = -1.0
    median = -1
    for num in pmf_list:
        curr = num
        if num < 0:
            print("Not a valid PMF")
            return None

        summ += num

        if curr > prev and median == -1:
            pass
        elif curr < prev and i > median:
            pass
        else:
            unimodal = False

        prev = curr

        if summ >= 0.5 and median == -1:
            median = pmf_list.index(num)
            print(f"The median is: {median + 1}")

    if unimodal:
        print("This PMF is a unimodal")


def strAsfouri(s):
    output = ""
    for char in s:
        # add char into output
        output += char
        if char != " ":
            output += "s"

    # return the result
    return output


r = None
dimension = None


def vol():
    pi = 3.1416
    global r, dimension
    global factor
    # collecting data if not previously assigned
    if r is None or dimension is None:
        r = float(input("Input a radius: "))
        dimension = int(input("Input the number of dimensions: "))
        # This is the factor used to multiply V(R)n-2 with
        factor = (2 * pi * (r ** 2)) / dimension

    else:
        # to account for (n-2):
        dimension -= 2
        #
        factor = factor * ((2 * pi * (r ** 2)) / dimension)

    print(factor)

    if dimension == 0:
        print(f"The volume is: {factor}")
    elif dimension == 1:
        print(f"The volume is: {factor*(2*r)}")
    else:
        vol()


def second_to_first():
    sequence = input("Enter sequence: ")

    tempo = ""
    numbers = []
    for char in sequence:
        if char == " ":
            numbers.append(int(tempo))
            tempo = ""
        else:
            tempo += char

    current_largest = 0
    second_largest = 0
    current_smallest = 0
    second_smallest = 0

    for i in range(0, len(numbers)):
        num = numbers[i]
        if i == 0:
            current_largest = num
            current_smallest = num
        elif i == 1:
            second_largest = num
            second_smallest = num
        else:
            # comparing the current largest with num to s
            if num > current_largest > second_largest:
                second_largest = current_largest
                current_largest = num
            if current_largest > num > second_largest:
                second_largest = num

            if current_smallest < num < current_smallest:
                second_smallest = current_smallest
                current_largest = num
            if num < second_smallest < current_smallest:
                second_smallest = num

    print(f"Second largest number is: {second_largest}, and second smallest number is: {second_smallest}")


def recPowerSlow(x, n):
    answer = 1
    if n == 0:
        return 1
    else:
        for i in range(0, abs(n)):
            answer *= x
        if n > 0:
            return answer
        else:
            return 1/answer


def recPowerFast(x, n):
    if n % 2 == 0:
        answer = recPowerFast(x, n/2)
        return answer*answer
    elif n % 2 == 1 and n != 1:
        return x*recPowerFast(x, n-1)
    elif n == 1:
        return x


def genBinStr2(n, m):
    n_bin = 2**n
    lst = []
    for i in range(0, n_bin):
        i_bin = bin(i)
        one_count = 0
        for char in str(i_bin):
            if char == "1":
                one_count += 1
        if one_count == m:
            i_bin = i_bin[2:]
            while len(i_bin) != n:
                i_bin = "0" + i_bin
            lst.append(i_bin)

    return lst

class ComplexNumbers:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.complex = complex(x, y)
        assert ((type(x) is int or type(x) is float) and (type(y) is int or type(y) is float)), "Bad Input!"

    def __str__(self):
        return str(self.complex)

    def __add__(self, other):
        return complex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return complex(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return complex((self.x * other.x) - (self.y * other.y), (self.x * other.y) + (self.y * other.x))

    def __truediv__(self, other):
        dividend = other.norm() ** 2
        assert dividend != 0, "Cannot divide by zero!"
        return complex(((self.x * other.x) + (self.y * other.y))/dividend, ((self.y * other.x) - (self.x * other.y))/dividend)

    def __neg__(self):
        return complex(-self.x, -self.y)

    def conj(self):
        return complex(self.x, -self.y)

    def norm(self):
        return (self.x**2 + self.y**2) ** (1/2)


class Vector(list):
    def __init__(self, other):
        assert len(other) != 0, "Invalid Input!"
        for e in other:
            assert type(e) == int or type(e) == float, "Invalid Input!"
        list.__init__(self, other)

    def __str__(self):
        lst = []
        for n in self:
            lst.append(n)
        return str(lst)

    def __add__(self, other):
        lst = []
        assert len(self) == len(other), "Unequal dimensions"
        for n in range(0, len(self)):
            lst.append(self[n] + other[n])
        return Vector(lst)

    def __sub__(self, other):
        lst = []
        assert len(self) == len(other), "Unequal dimensions"
        for n in range(0, len(self)):
            lst.append(self[n] - other[n])
        return Vector(lst)

    def __mul__(self, other):
        answer = 0
        assert len(self) == len(other), "Unequal dimensions"
        for n in range(0, len(self)):
            answer += self[n] * other[n]
        return answer

    def __neg__(self):
        lst = []
        for n in range(0, len(self)):
            lst.append(-self[n])
        return Vector(lst)

    def norm(self):
        answer = 0
        for n in range(0, len(self)):
            answer += self[n] ** 2
        return answer ** (1/2)


def zeros(n):
    assert type(n) is int, "Argument only accepts integers."
    return [0] * n


def ones(n):
    assert type(n) is int, "Argument only accepts integers."
    return [1] * n


i = Vector([1, 2, 3])
j = Vector([4, 5, 6])
print(-i + ones(3))