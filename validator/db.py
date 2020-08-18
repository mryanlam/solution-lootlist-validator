from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, Person, Item, ItemList
from typing import Dict, List

class SolutionLootDB():
    def __init__(self):
        engine = create_engine("sqlite:///solution_loot.db")
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def insert_person(self, name: str):
        self.session.add(Person(name=name))
        self.session.commit()
    
    def list_person(self) -> List[str]:
        return[ x.name for x in self.session.query(Person).all() ]

    def list_lootlist(self, raider_name: str):
        return [{50: "Test ITEM"}, {49: "TF BLESSED"}]

if __name__ == '__main__':
    db = SolutionLootDB()
    db.session.add(Person(name='Charurun'))
    db.session.add(Person(name='Tenju'))
    db.session.commit()