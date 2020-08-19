from typing import Dict, List, Tuple
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from itertools import zip_longest
from db import SolutionLootDB
import pprint

MAX_ALLOCATION = 3
MAX_DUPLICATE_ITEM_TYPE = 1

def validate_sheet(uri: str) -> Dict[str, str]:
    loot_list_dict = _get_sheet(uri)
    for k, v in loot_list_dict.items():
        print("{}| {}".format(k, v))
    print("Validating sheet")
    valid, err_msg_dict = (_validate_sheet(loot_list_dict))
    pp = pprint.PrettyPrinter(indent=4)
    print("Sheet validity {}".format(valid))
    pp.pprint(err_msg_dict)


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

def _validate_sheet(loot_list: Dict[int, Tuple]) -> Tuple[bool, Dict]:
    colored_brackets = [[50, 49, 48], [47, 46, 45], [44, 43, 42], [41, 40, 39]]
    db = SolutionLootDB()
    overall_valid = True
    info_dict = dict()
    for bracket in colored_brackets:
        valid, info = (_validate_bracket(loot_list, bracket, db))
        if not valid:
            overall_valid = False
            info_dict[str(bracket)] = info
    # TODO Validate non bracketed items
    return (overall_valid, info_dict)

# TODO Validate Class
def _validate_bracket(loot_list: Dict[int, Tuple], bracket: List[int], db: SolutionLootDB) -> Tuple[bool, List[str]]:
    allocation_sum = 0
    type_count = dict()
    valid = True
    info = list()
    for k in bracket:
        if k in loot_list:
            for item in loot_list[k]:
                if not item:
                    continue
                item_attr = db.get_item_by_name(item)
                allocation_sum += item_attr["allocation"]
                type_count[item_attr["item_type"]] = type_count.get(item_attr["item_type"], 0) + 1
    if allocation_sum > MAX_ALLOCATION:
        valid = False
        info.append("Number of allocation points {} exceeds the max {}".format(allocation_sum, MAX_ALLOCATION))
    for item_type, count in type_count.items():
        if count > MAX_DUPLICATE_ITEM_TYPE:
            valid = False
            info.append("Number of {} in bracket {} exceeds the max {}".format(item_type, count, MAX_DUPLICATE_ITEM_TYPE))
    return (valid, info)
    


if __name__ == '__main__':
    validate_sheet("https://docs.google.com/spreadsheets/d/1ZnGUeif6qvAT9IjgI5QdtCh0lTIuweWaXGeCjVQcF7M/edit?usp=sharing")