from . import db, models

import random

difficulties = {
    'easy': 100*100, # $100,
    'medium': 75*100, # $100,
    'hard': 50*100, # $100,
    'ultra': 25*100 # $100
}

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

# customers start with this amount of money
starting_money = 20*100

def increment_simulation():
    """
        loops through customers and decides if they enter a shop and / or buy something

        returns log entries
    """
    log = []

    for i in range(0, base_spawn_rate):
        log.append(db.create_customer(starting_money=starting_money))

    with db.get_session() as session:
        customers = db.get_all(session, models.Customer)
        shops = db.get_all(session, models.Shop)
        for customer in customers:
            modified_weights = action_weights.copy()
            # each shop provides a 10% boost to the weight of going to a shop
            modified_weights[1] = modified_weights[1]*(1 + 0.1*len(shops))
            # each customer provides a 5% boost to the weight of leaving the game
            # if the customer has >= $10, they ignore the base weight for leaving
            # if the customer has < $5, it doubles the weight for leaving
            wealth_factor = 1
            if customer.money >= 10*100:
                wealth_factor = 0
            elif customer.money < 5*100:
                wealth_factor = 2
            modified_weights[2] = modified_weights[2]*(wealth_factor + 0.05*len(customers))
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
            else:
                raise ValueError(f"Invalid action - {action}")
    return log
