from typing import List, Dict
import gspread
from create_db import Item
from db import SolutionLootDB
import pprint

def populate_item_db(uri: str, raid : str):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_url(uri).sheet1
    item_list = list()
    db = SolutionLootDB()
    pp = pprint.PrettyPrinter(indent=4)
    if raid == "BWL":
        # loot_list = sh.get("G15:N174")
        print("BWL is not yet implemented")
        # TODO: Normalize the classes/specs in prios to match AQ style
    if raid == "AQ":
        # Item, Allocation, Type, Designation, First Priority, Second Priority
        loot_list = sh.get("G15:N131")
        for row in loot_list:
            pp.pprint(row)
            if len(row) < 8:
                item_list.append(Item(item_name=row[0],
                                    allocation=row[1],
                                    item_type=row[2],
                                    designation=row[3],
                                    first_prio=row[6],
                                    second_prio=None,
                                    raid="AQ40"))
            else:
                item_list.append(Item(item_name=row[0],
                                    allocation=row[1],
                                    item_type=row[2],
                                    designation=row[3],
                                    first_prio=row[6],
                                    second_prio=row[7],
                                    raid="AQ40"))
            # item_list.append({"item_name":row[0],
            #                         "allocation":row[1],
            #                         "item_type":row[2],
            #                         "designation":row[3],
            #                         "first_prio":row[4],
            #                         "second_prio":row[5],
            #                         "raid":"AQ40"})
    elif raid == "NAXX":
        # Item, Allocation, Type, Designation, First Priority, Second Priority
        loot_list = sh.get("G15:N135")
        for row in loot_list:
            pp.pprint(row)
            if len(row) < 8:
                item_list.append(Item(item_name=row[0],
                                    allocation=row[1],
                                    item_type=row[2],
                                    designation=row[3],
                                    first_prio=row[6],
                                    second_prio=None,
                                    raid="NAXX"))
            else:
                item_list.append(Item(item_name=row[0],
                                    allocation=row[1],
                                    item_type=row[2],
                                    designation=row[3],
                                    first_prio=row[6],
                                    second_prio=row[7],
                                    raid="NAXX"))

    db.insert_items(item_list)

if __name__ == '__main__':
    # AQ40
    # populate_item_db("https://docs.google.com/spreadsheets/d/1gaCOz-wRpey_YghJwYD54ftV-pxx5348O8dPpyn5IcI/edit#gid=0", "AQ")
    # BWL/MC/ONY
    # populate_item_db("https://docs.google.com/spreadsheets/d/1wbCuQxeZzAOPPmfCXVaYXL-eZh91L5NQxc6lZ0i2Nk0/edit#gid=0", "BWL")
    populate_item_db("https://docs.google.com/spreadsheets/d/19bGumU9iCaYuvi7j1y7wQdKpx_0RLg0pxt40k2Gur4M/edit#gid=0", "NAXX")