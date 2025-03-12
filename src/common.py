
import random

shop_types = [
    'Tacos',
    'Pancakes',
    'Burritos',
]

available_menu_items = [
    ('Rolled Taco', 1.50*100),
    ('Strawberry Pancakes', 5.00*100),
    ('Cali Burrito', 8.00*100),
    ('Loaded Taco', 2.15*100),
    ('DoubleStuffed Burrito', 12.00*100)
]

base_profit_margin = 0.15

def get_random_menu():
    """select between 1 and 2 random menu items"""
    number_of_items = random.randint(1, 2)
    return random.sample(available_menu_items, k=number_of_items)

def get_random_name():
    with open("static/names.txt") as infile:
        names = [ line for line in infile.readlines() ]
        name = names[random.randint(0, len(names)-1)]
        return name.replace('\n', '')

def get_random_shop_name():
    person_name = get_random_name().split(" ")[0]
    chosen_shop_type = random.choice(shop_types)
    return f"{person_name}'s {chosen_shop_type}"