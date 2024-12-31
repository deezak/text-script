import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Authenticate and connect to Google Sheets API
def authenticate_gsheet():
    # Path to your credentials.json file
    creds = Credentials.from_service_account_file(
        'google-auth.json',
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # Authenticate and return the gspread client
    gc = gspread.authorize(creds)
    return gc

# Change the color of a specific cell
def change_cell_color(spreadsheet_id, cell, color):
    gc = authenticate_gsheet()

    # Open the spreadsheet by its ID
    spreadsheet = gc.open_by_key(spreadsheet_id)

    # Select the first sheet
    sheet = spreadsheet.sheet1

    # Update the cell color using the API
    sheet.format(cell, {
        'backgroundColor': {
            'red': color[0],  # red component of the RGB
            'green': color[1],  # green component of the RGB
            'blue': color[2],  # blue component of the RGB
        }
    })
    print(f"Cell {cell} color changed to {color}.")

# Example usage
spreadsheet_id = '1fNMBn3BFDCrUxxbqAALXJOR58beMU7-oDkziTQG707g'
cell = 'A1'  # Change color of cell A1
color = (1.0, 0.0, 0.0)  # RGB color (red in this case)
change_cell_color(spreadsheet_id, cell, color)
