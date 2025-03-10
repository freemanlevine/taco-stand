from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass

class Shop(Base):
    """A shop that sells goods to customers"""
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Shop(id={self.id!r}, name={self.name!r})"

class Customer(Base):
    """A customer that can buy goods from one or more shops"""
    __tablename__ = "customer"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, name={self.name!r})"

# class MenuItem(Base):
#     """Something that can be sold by shops to customers"""
#     __tablename__ = "menu_item"
    
#     def __init__(self, name):
#         self.name = name
