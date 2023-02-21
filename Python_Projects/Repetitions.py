def repeating_boi():
    sequence = input()

    rep_char = "O"
    rep_count = 1
    highest_rep = 1
    for ele in sequence:
        if rep_char == ele:
            rep_count += 1
        else:
            if rep_count > highest_rep:
                highest_rep = rep_count
            rep_count = 1
            rep_char = ele

    if rep_count > highest_rep:
        highest_rep = rep_count

    print(highest_rep)


repeating_boi()