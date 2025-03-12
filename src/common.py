
import random

def get_random_name():
    with open("static/names.txt") as infile:
        names = [ line for line in infile.readlines() ]
        name = names[random.randint(0, len(names))]
        return name.replace('\n', '')
