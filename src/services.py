import sqlite3
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session

from . import models
from .models import Shop, Customer, MenuItem

def get_engine():
    return create_engine("sqlite:///db/database.db", echo=False)

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

def purchase_item(customer_id, menu_item_id):
    engine = get_engine()
    with Session(engine) as session:
        customer = get_by_id(session, Customer, customer_id)
        menu_item = get_by_id(session, MenuItem, menu_item_id)
        shop = get_by_id(session, Shop, menu_item.shop_id)
        customer.money = customer.money - menu_item.cost
        print("Customer {} purchased {} from {} and has ${} left!".format(
            customer.name,
            menu_item.name,
            shop.name,
            customer.money/100.0
        ))
        session.commit()
