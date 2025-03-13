import sqlite3
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import os

from . import models
from .models import Shop, Customer, MenuItem

from . import common

DB_PATH = "db/database.db"

def get_engine():
    return create_engine("sqlite:///{}".format(DB_PATH), echo=False)

def get_session():
    return Session(get_engine())

def delete_db():
    os.remove(DB_PATH)

def init_db():
    engine = get_engine()
    with engine.connect() as conn:
        try:
            existing_shops = conn.execute(text("select count(*) from shop")).fetchall()[0][0]
            if existing_shops:
                print("db already init")
                return
        except:
            pass
    with Session(engine) as session:
        models.Base.metadata.create_all(engine)

        dannys_tacos = Shop(name="Danny's Tacos", menu_items=[
            MenuItem(name="Street Taco", cost=0.75*100),
            MenuItem(name="Rolled Taco", cost=1.00*100)
        ])
        customers = [
            Customer(name="Jen", money=10.00*100),
            Customer(name="Freeman", money = 5.00*100)
        ]
        session.add_all([dannys_tacos, *customers])
        session.commit()

def get_by_id(session, object_type, id):
    return session.scalars(select(object_type).where(object_type.id == id)).one()

def get_all(session, object_type):
    return session.scalars(select(object_type)).all()

def purchase_item(session, player_id, customer_id, menu_item_id):
    customer = get_by_id(session, Customer, customer_id)
    menu_item = get_by_id(session, MenuItem, menu_item_id)
    player = get_by_id(session, models.Player, player_id)
    money_remaining = customer.money - menu_item.cost
    player_commission = menu_item.cost * common.base_profit_margin
    player_money_after = player.money + player_commission
    if money_remaining < 0:
        message = "{name} doesn't have enough money!\n{item_name} costs ${item_cost:,.2f} and {name} has ${amount:,.2f} left".format(
            name = customer.name,
            item_name = menu_item.name,
            item_cost = menu_item.cost/100.0,
            amount = customer.money/100.0
        )
    else:
        customer.money = money_remaining
        player.money = player_money_after
        session.commit()
        message = "Customer {} purchased {} for ${:,.2f} and has ${:,.2f} left!".format(
            customer.name,
            menu_item.name,
            menu_item.cost/100.0,
            customer.money/100.0
        )
        message += f" Player {player.name} earned ${player_commission/100.0:,.2f} from the sale and now has ${player.money/100.0:,.2f}."
    print(message)
    return message

def get_menu_items(session, shop_id):
    """returns a list of menu items belonging to a given shop"""
    return list(session.scalars(
        select(models.MenuItem)
        .where(models.MenuItem.shop_id == shop_id)
    ))

def create_player(player_name, starting_money=0):
    if player_name == '':
        raise ValueError("Can't create player with empty name.")
    engine = get_engine()
    with Session(engine) as session:
        new_player = models.Player(
            name=player_name,
            money=starting_money
        )
        session.add(new_player)
        session.commit()
        return new_player.id

def get_active_player():
    engine = get_engine()
    with Session(engine) as session:
        active_player = session.scalars(select(models.ActivePlayer)).one()
        if active_player:
            print(f'active player {active_player.player.name} found')
            return active_player.player
        else:
            print(f'no active player found')
            raise Exception("No Active Player Found")
        
def set_active_player(player_id):
    engine = get_engine()
    with Session(engine) as session:
        next_player = get_by_id(session, models.Player, player_id)
        try:
            active_player = session.scalars(select(models.ActivePlayer)).one()
            active_player.player_id = next_player.id
            active_player.player = next_player
            session.commit()
            return active_player.player
        except:
            active_player = models.ActivePlayer(
                player_id = next_player.id,
                player=next_player
            )
            session.add(active_player)
            session.commit()
            return active_player.player

def delete_player(player_id):
    engine = get_engine()
    with Session(engine) as session:
        player = get_by_id(session, models.Player, player_id)
        try:
            active_player = session.scalars(select(models.ActivePlayer)).one()
            if active_player.player_id == player_id:
                raise ValueError("Can't delete active player")
        except NoResultFound:
            ## continue with delete if no active player is found
            pass
        session.delete(player)
        session.commit()

def build_shop(created_by_player_id, shop_price):
    with get_session() as session:
        player = get_by_id(session, models.Player, created_by_player_id)
        try:
            menu_items = [
                models.MenuItem(name=item_data[0], cost=item_data[1])
                for item_data in common.get_random_menu()
            ]
            created_shop = models.Shop(
                name=common.get_random_shop_name(),
                owned_by=created_by_player_id,
                menu_items=menu_items
            )
            player.money = player.money - shop_price
            if player.money < 0.0:
                raise ValueError("Insufficient funds")
            session.add(created_shop)
            session.commit()
            message = f"{player.name} built {created_shop.name} for ${shop_price/100.0:,.2f}"
            message += f" and has ${player.money/100.0:,.2f} remaining."
            return message
        except ValueError:
            return f"{player.name} failed to build a shop due to insufficient funds."
        
def create_customer(starting_money=10*100):
    with get_session() as session:
        customer = models.Customer(
            name=common.get_random_name(),
            money=starting_money
        )
        session.add(customer)
        session.commit()
        return f"Customer {customer.name} created with ${customer.money/100:,.2f}"

def delete_shop(shop_id):
    with get_session() as session:
        shop = get_by_id(session, Shop, shop_id)
        session.delete(shop)
        session.commit()
