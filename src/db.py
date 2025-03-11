import sqlite3
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import os

from . import models
from .models import Shop, Customer, MenuItem

DB_PATH = "db/database.db"

def get_engine():
    return create_engine("sqlite:///{}".format(DB_PATH), echo=False)

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

def purchase_item(customer_id, menu_item_id):
    engine = get_engine()
    with Session(engine) as session:
        customer = get_by_id(session, Customer, customer_id)
        menu_item = get_by_id(session, MenuItem, menu_item_id)
        shop = get_by_id(session, Shop, menu_item.shop_id)
        money_remaining = customer.money - menu_item.cost
        if money_remaining < 0:
            print("{name} doesn't have enough money!\n{item_name} costs ${item_cost:,.2f} and {name} has ${amount:,.2f} left".format(
                name = customer.name,
                item_name = menu_item.name,
                item_cost = menu_item.cost/100.0,
                amount = customer.money/100.0
            ))
        else:
            customer.money = money_remaining
            session.commit()
            print("Customer {} purchased {} from {} and has ${:,.2f} left!".format(
                customer.name,
                menu_item.name,
                shop.name,
                customer.money/100.0
            ))

def get_menu_items(session, shop_id):
    """returns a list of menu items belonging to a given shop"""
    return list(session.scalars(
        select(models.MenuItem)
        .where(models.MenuItem.shop_id == shop_id)
    ))

def create_player(player_name, starting_money=0):
    engine = get_engine()
    with Session(engine) as session:
        new_player = models.Player(
            name=player_name,
            money=starting_money
        )
        session.add(new_player)
        session.commit()

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
