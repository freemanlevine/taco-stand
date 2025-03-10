import sqlite3
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session

from . import models

def get_engine():
    return create_engine("sqlite:///db/database.db", echo=True)


def init_db():
    engine = get_engine()
    with engine.connect() as conn:
        existing_shops = conn.execute(text("select count(*) from shop")).fetchall()[0][0]
        if existing_shops:
            print("db already init")
            return
    with Session(engine) as session:
        models.Base.metadata.create_all(engine)

        dannys_tacos = models.Shop(name="Danny's Tacos")
        session.add(dannys_tacos)
        customers = [
            models.Customer(name="Jen"),
            models.Customer(name="Freeman")
        ]
        session.add_all(customers)
        session.commit()
