from typing import Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from itertools import zip_longest

def validate_sheet(uri: str) -> Dict[str, str]:
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(uri).sheet1
    col_1 = sheet.get("B6:C55")
    # col_2 = sheet.get("C6:C55")
    val = 50
    for row in col_1:
        try:
            left = row[0]
        except IndexError:
            left = None
        try:
            right = row[1]
        except IndexError:
            right = None
        print("{} {} {}".format(val, left, right))
        val -= 1



if __name__ == '__main__':
    validate_sheet("https://docs.google.com/spreadsheets/d/1ZnGUeif6qvAT9IjgI5QdtCh0lTIuweWaXGeCjVQcF7M/edit?usp=sharing")