from . import db, models

import random

customer_actions = [
    'do_nothing',
    'go_to_shop',
]

shop_price = 20*100 # $20.00

def increment_simulation():
    """
        loops through customers and decides if they enter a shop and / or buy something

        returns log entries
    """
    log = []
    with db.get_session() as session:
        customers = db.get_all(session, models.Customer)
        shops = db.get_all(session, models.Shop)
        for customer in customers:
            action = random.choice(customer_actions)
            log += f'customer chose {action}'
            if action == 'go_to_shop':
                chosen_shop = random.choice(shops)
                chosen_menu_item = random.choice(chosen_shop.menu_items)
                log += db.purchase_item(customer.id, chosen_menu_item.id)
    return log