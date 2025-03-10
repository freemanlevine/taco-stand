import sqlite3
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session

from . import models

def get_engine():
    return create_engine("sqlite:///db/database.db", echo=True)


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

        dannys_tacos = models.Shop(name="Danny's Tacos", menu_items=[
            models.MenuItem("Street Taco"),
            models.MenuItem("Rolled Taco")
        ])
        customers = [
            models.Customer(name="Jen"),
            models.Customer(name="Freeman")
        ]
        session.add_all([dannys_tacos, *customers])
        session.commit()
