from . import db, models

welcome_text = """
Welcome to Taco Stand!
"""

def input_menu_number(msg):
    user_input = input(msg)
    try:
        return int(user_input)
    except:
        print("Invalid input")

def input_select_object(objects, object_name):
    msg = "Select a {}:\n".format(object_name)
    for index in range(1, len(objects) + 1):
        msg += "{}. {} \n".format(
            index, objects[index-1].name
        )
    menu_number = input_menu_number(msg)
    selected_object = objects[menu_number-1]
    print("{} was selected".format(selected_object.name))
    return selected_object


def input_select_from_all_objects(session, object_type):
    objects = db.get_all(session, object_type)
    return input_select_object(objects, object_type.__tablename__)


def handle_purchase_item():
    engine = db.get_engine()
    with db.Session(engine) as session:
        # allow the user to choose a customer
        customer = input_select_from_all_objects(session, models.Customer)

        # allow the user to choose a shop
        shop = input_select_from_all_objects(session, models.Shop)

        # allow the user to choose a menu item
        shop.print_menu()
        user_input = input_menu_number("Enter the number of the item you wish to purchase.\n")
        menu_item = shop.menu_items[user_input-1]

        db.purchase_item(customer.id, menu_item.id)

def handle_display_menu():
    engine = db.get_engine()
    with db.Session(engine) as session:
        # choose a shop whose menu we will display
        shop = input_select_from_all_objects(session, models.Shop)
        shop.print_menu()
        user_input = input_menu_number("1. Purchase an item\n2. Return to main menu\n")
        if user_input == 1:
            user_input = input_menu_number("Enter the number of the item you wish to purchase.\n")
            menu_item = shop.menu_items[user_input-1]
            customer = input_select_from_all_objects(session, models.Customer)
            db.purchase_item(customer.id, menu_item.id)

options_menu = """
Please select from the following options.

1. Purchase Menu Item
2. Display Shop Menu
"""
    
menu_handlers = {
    1: handle_purchase_item,
    2: handle_display_menu
}

def run():
    print(welcome_text)
    while True:
        try:
            menu_number = input_menu_number(options_menu)
            menu_handlers[menu_number]()
        except Exception as e:
            print("Error while running application", e)
            break


if __name__ == '__main__':
    run()
