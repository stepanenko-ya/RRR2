with open("qwerty") as file:
    lst = file.readlines()
    for i in lst:
        el = i.split("|")
        print(el[-2:])