import os
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1fNMBn3BFDCrUxxbqAALXJOR58beMU7-oDkziTQG707g'  # Replace with your Google Sheet ID
RANGE_NAME = 'Sheet1!A9'  # Cell to increment (e.g., A1)

def authenticate_with_service_account():
    """Authenticate using the service account."""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # Path to your service account credentials file
    SERVICE_ACCOUNT_FILE = 'creds.json'  # Replace with the path to your service account JSON file

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Create the Sheets API client
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_current_value(service):
    """Get the current value of the cell from the spreadsheet."""
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    value = result.get('values', [])
    if not value:
        print("No data found.")
        return 0  # Return a default value if the cell is empty
    else:
        return int(value[0][0])  # Assuming the cell contains an integer

def update_value(service, value):
    """Update the cell with the incremented value."""
    values = [[value]]  # The new value to set
    body = {
        'values': values
    }
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption="RAW", body=body).execute()

def main():
    """Increment the value of the specified cell."""
    service = authenticate_with_service_account()

    current_value = get_current_value(service)
    new_value = current_value + 1

    update_value(service, new_value)
    print(f"Value updated: {current_value} -> {new_value}")

if __name__ == '__main__':
    main()