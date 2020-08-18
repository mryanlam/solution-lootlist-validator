from typing import Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def validate_sheet(uri: str) -> Dict[str, str]:
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(uri).sheet1
    records = sheet.get_all_records()
    print(records)

if __name__ == '__main__':
    validate_sheet("https://docs.google.com/spreadsheets/d/1ZnGUeif6qvAT9IjgI5QdtCh0lTIuweWaXGeCjVQcF7M/edit?usp=sharing")