
import random

shop_types = [
    'Tacos',
    'Pancakes',
    'Burritos',
    'Diner',
    'Restaurant',
    'Cafe'
]
base_foods = [
    ('Taco', 1.00*100),
    ('Pancakes', 4.00*100),
    ('Burrito', 6.00*100),
    ('Salad', 5.00*100),
    ('Smoothie', 8.00*100)
]

modifiers = [
    ('Rolled', 1.25),
    ('Stuffed', 1.5),
    ('Strawberry', 1.75),
    ('Chicken', 2.0),
    ('Loaded', 2.25),
    ('DoubleStuffed', 2.5)
]

base_profit_margin = 0.15

def make_random_menu_item():
    base_food = random.choice(base_foods)
    modifier = random.choice(modifiers)
    return ( f"{modifier[0]} {base_food[0]}", base_food[1] * modifier[1] )

def get_random_menu():
    """select between 2 and 5 random menu items"""
    number_of_items = random.randint(1, 5)
    return [
        make_random_menu_item()
        for i in range(0, number_of_items)
    ]

def get_random_name():
    with open("static/names.txt") as infile:
        names = [ line for line in infile.readlines() ]
        name = names[random.randint(0, len(names)-1)]
        return name.replace('\n', '')

def get_random_shop_name():
    person_name = get_random_name().split(" ")[0]
    chosen_shop_type = random.choice(shop_types)
    return f"{person_name}'s {chosen_shop_type}"