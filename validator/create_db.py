from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    spec = Column(String(250), nullable=False)
    """
    spec is going to be a bit overloaded.
    Tnk = War
    Ret = Pal
    Frl = Dru
    Mag
    Wlk
    Hnt
    Pri
    Rog
    All
    """
 
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(250))
    item_type = Column(String(250))
    designation = Column(String(250), nullable=False)
    allocation = Column(Integer)

class ItemList(Base):
    __tablename__ = 'itemlist'
    id = Column(Integer, primary_key=True)
    person = Column(Integer, ForeignKey('person.id'))
    item = Column(Integer, ForeignKey('item.id'))
    value = Column(Integer)

engine = create_engine("sqlite:///solution_loot.db")
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)