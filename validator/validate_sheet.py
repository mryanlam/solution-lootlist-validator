from typing import Dict, List, Tuple
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from itertools import zip_longest
from db import SolutionLootDB
import pprint

MAX_ALLOCATION = 3
MAX_DUPLICATE_ITEM_TYPE = 1
VALID_SPEC = ["tnk", "war", "ret", "pal", "frl", "dru", "mag","wlk","hnt", "pri", "rog", "all"]

def validate_sheet(c: str, uri: str) -> Dict[str, str]:
    if not c:
        raise ValueError("Invalid Argument class set to {}".format(c))
    if c.lower() not in VALID_SPEC:
        raise ValueError("Invalid Class")
    if not uri:
        raise ValueError("Invalid Argument lootsheet not found")
    loot_list_dict = _get_sheet(uri)
    # for k, v in loot_list_dict.items():
    #     print("{}| {}".format(k, v))
    print("Validating sheet")
    valid, err_msg_dict = (_validate_sheet(c, loot_list_dict))
    pp = pprint.PrettyPrinter(indent=4)
    print("Sheet validity {}".format(valid))
    pp.pprint(err_msg_dict)
    return (valid, err_msg_dict)


def _get_sheet(uri: str) -> Dict[int, Tuple]:
    """
    Extract lootlist from spreadsheet and return dict of items and values
    """
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_url(uri).sheet1
    loot_list = sh.get("B6:C55")
    ret = dict()
    val = 51
    for row in loot_list:
        val -= 1
        try:
            left = row[0]
        except IndexError:
            left = None
        try:
            right = row[1]
        except IndexError:
            right = None
        if not left and not right:
            continue
        ret[val] = (left, right)
    return ret

def _validate_sheet(c: str, loot_list: Dict[int, Tuple]) -> Tuple[bool, Dict]:
    colored_brackets = [[50, 49, 48], [47, 46, 45], [44, 43, 42], [41, 40, 39]]
    other_brackets = [x for x in range(1, 39)]
    special_class_map = {   "tnk": ["tnk", "war"],
                            "war": ["war", "fur"], 
                            "ret": ["ret", "pal"], 
                            "frl": ["frl", "dru"]}
    db = SolutionLootDB()
    overall_valid = True
    info_dict = dict()
    player_class = [c]
    if c in special_class_map:
        player_class = special_class_map[c]
    for bracket in colored_brackets:
        valid, info = (_validate_bracket(player_class, loot_list, bracket, db))
        if not valid:
            overall_valid = False
            info_dict[str(bracket)] = info
    valid, info = (_validate_non_bracket(player_class, loot_list, other_brackets, db))
    if not valid:
        overall_valid = False
        info_dict["non bracketed"] = info
    return (overall_valid, info_dict)

def _validate_bracket(class_list: List[str], loot_list: Dict[int, Tuple], bracket: List[int], db: SolutionLootDB) -> Tuple[bool, List[str]]:
    valid = True
    allocation_sum = 0
    type_count = dict()
    info = list()
    non_prio_items = list()
    for k in bracket:
        if k in loot_list:
            for item in loot_list[k]:
                if not item:
                    continue
                try:
                    item_attr = db.get_item_by_name(item)
                except Exception as e:
                    raise ValueError("Invalid item {} causes {}".format(item, e))
                allocation_sum += item_attr["allocation"]
                type_count[item_attr["item_type"]] = type_count.get(item_attr["item_type"], 0) + 1
                found = False
                for c in class_list:
                    if c in item_attr["first_prio"].lower() or 'all' in item_attr["first_prio"].lower():
                        found = True
                if not found:
                    non_prio_items.append(item)
                    print(item_attr["first_prio"].lower())
    if allocation_sum > MAX_ALLOCATION:
        valid = False
        info.append("Number of allocation points {} exceeds the max {}".format(allocation_sum, MAX_ALLOCATION))
    for item_type, count in type_count.items():
        if count > MAX_DUPLICATE_ITEM_TYPE:
            valid = False
            info.append("Number of {} in bracket {} exceeds the max {}".format(item_type, count, MAX_DUPLICATE_ITEM_TYPE))
    if len(non_prio_items) > 0:
        valid = False
        info.append("Items {} are not First Prio for {}".format(non_prio_items, class_list[0]))
    return (valid, info)

def _validate_non_bracket(class_list: List[str], loot_list: Dict[int, Tuple], bracket: List[int], db: SolutionLootDB) -> Tuple[bool, List[str]]:
    valid = True
    info = list()
    non_prio_items = list()
    for k in bracket:
        if k in loot_list:
            for item in loot_list[k]:
                if not item:
                    continue
                try:
                    item_attr = db.get_item_by_name(item)
                except Exception as e:
                    raise ValueError("Invalid item {} causes {}".format(item, e))
                found = False
                for c in class_list:
                    if c in item_attr["first_prio"].lower() or 'all' in item_attr["first_prio"].lower():
                        found = True
                    if item_attr["second_prio"] is not None:
                        if c in item_attr["second_prio"].lower() or 'all' in item_attr["second_prio"].lower():
                            found = True
                if not found:
                    non_prio_items.append(item)
    
    if len(non_prio_items) > 0:
        valid = False
        info.append("Items {} are not First or Second Prio for {}".format(non_prio_items, class_list[0]))
    return (valid, info)

if __name__ == '__main__':
    # validate_sheet("tnk", "https://docs.google.com/spreadsheets/d/1ZnGUeif6qvAT9IjgI5QdtCh0lTIuweWaXGeCjVQcF7M/edit?usp=sharing")
    validate_sheet("wlk", "https://docs.google.com/spreadsheets/d/1G29l-pmDxmR-DslJEh2ODdtrKVNWu2ZijkM2LOiJURM/edit#gid=0")