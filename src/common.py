
import random

shop_types = [
    'Tacos',
    'Pancakes',
    'Burritos',
    'Chimichangas'
]

def get_random_name():
    with open("static/names.txt") as infile:
        names = [ line for line in infile.readlines() ]
        name = names[random.randint(0, len(names))]
        return name.replace('\n', '')

def get_random_shop_name():
    person_name = get_random_name().split(" ")[0]
    chosen_shop_type = random.choice(shop_types)
    return f"{person_name}'s {chosen_shop_type}"