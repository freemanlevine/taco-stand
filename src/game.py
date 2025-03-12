from . import db, models

import random

customer_actions = [
    'do_nothing',
    'go_to_shop',
    'leave_game'
]

action_weights = [
    35, 25, 10
]

# $20.00
shop_price = 20*100 

# number of customers spawned by the game per round
base_spawn_rate = 2

# all customers receive this every round that they do nothing
background_income = 2.00*100

def increment_simulation():
    """
        loops through customers and decides if they enter a shop and / or buy something

        returns log entries
    """
    log = []

    for i in range(0, base_spawn_rate):
        log.append(db.create_customer())

    with db.get_session() as session:
        customers = db.get_all(session, models.Customer)
        shops = db.get_all(session, models.Shop)
        active_player = db.get_active_player()
        for customer in customers:
            modified_weights = action_weights.copy()
            # each shop provides a 10% boost to the weight of going to a shop
            modified_weights[1] = modified_weights[1]*(1 + 0.1*len(shops))
            # each customer provides a 5% boost to the weight of leaving the game
            modified_weights[2] = modified_weights[2]*(1 + 0.05*len(customers))
            action = random.choices(customer_actions, weights=modified_weights, k=1)[0]
            if action == 'go_to_shop':
                if len(shops) == 0:
                    log.append(f'Customer {customer.name} couldn\'t buy anything because there are no shops!')
                    continue
                chosen_shop = random.choice(shops)
                chosen_menu_items = random.choices(chosen_shop.menu_items, k=random.randint(1, len(chosen_shop.menu_items)))
                log.append(f'Customer {customer.name} is heading to {chosen_shop.name} and wants {len(chosen_menu_items)} items')
                for item in chosen_menu_items:
                    log.append(db.purchase_item(session, chosen_shop.owned_by, customer.id, item.id))
                session.commit()
            elif action == 'do_nothing':
                customer.money = customer.money + background_income
                session.commit()
                log.append(f'Customer {customer.name} earned ${background_income/100:,.2f}')
            elif action == 'leave_game':
                session.delete(customer)
                session.commit()
                log.append(f'Customer {customer.name} left the game')
    return log
