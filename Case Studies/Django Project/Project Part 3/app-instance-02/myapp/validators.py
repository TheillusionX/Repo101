def validate_int(integer, num):
    if integer < 10**num or integer >= 10**(num + 1):
        return False
    else:
        return True

def validate_phone_number(phone_number_string):
    if phone_number_string[0] != "+":
        return None
    else:
        phone_number_string = phone_number_string[1:]
    try:
        return int(phone_number_string)
    except:
        return None