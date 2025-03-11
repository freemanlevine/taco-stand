from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import MetaData
from sqlalchemy import String, ForeignKey, Integer
from typing import List


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

class Shop(Base):
    """A shop that sells goods to customers"""
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    menu_items: Mapped[List["MenuItem"]] = relationship()

    def __repr__(self) -> str:
        return f"Shop(id={self.id!r}, name={self.name!r})"

class Customer(Base):
    """A customer that can buy goods from one or more shops"""
    __tablename__ = "customer"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    money: Mapped[int] = mapped_column(Integer, default=1000) # in cents

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, name={self.name!r}, money=${self.money/100.0})"

class MenuItem(Base):
    """Something that can be sold by shops to customers"""
    __tablename__ = "menu_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    cost: Mapped[int] = mapped_column(Integer) #in cents
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))

    def __repr__(self) -> str:
        return f"MenuItem(id={self.id!r}, name={self.name!r}, cost=${self.cost/100.0}, shop_id={self.shop_id})"
