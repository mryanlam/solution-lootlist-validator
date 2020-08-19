from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from create_db import Base, Person, Item, ItemList
from typing import Dict, List

class SolutionLootDB():
    """
    Class that handles database queries to our sqlite db
    """
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

    def insert_items(self, item_list: List[Dict]):
        for item in item_list:
            self.session.add(item)
        self.session.commit()

    def get_item_by_name(self, item_name) -> Dict[str, str]:
        query = self.session.query(Item).filter(Item.item_name==item_name).first()
        return self.object_as_dict(query)

    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

if __name__ == '__main__':
    db = SolutionLootDB()
    db.session.add(Person(name='Charurun', spec="Tnk"))
    db.session.add(Person(name='Tenju', spec="Hnt"))
    db.session.commit()
