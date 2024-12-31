import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from twilio.rest import Client
import phonenumbers
# Twilio credentials (replace with your own from Twilio dashboard)
ACCOUNT_SID = 'ACebe59a36b27abef4fb3829ddbebfafbf'
AUTH_TOKEN = 'd3bc13d29421d4f8c000944c717f2c20'
TWILIO_PHONE_NUMBER = '+18665357389'

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Initialize Twilio client
textClient = Client(ACCOUNT_SID, AUTH_TOKEN)


# Load Excel sheet
contacts_df = pd.read_excel("test-contact.xlsx")

# Function to send personalized messages
def send_personalized_texts():
    for index, row in contacts_df.iterrows():
        name = row['Name']
        print(row["Phone Number"])
        phone_number = "+1"+str(row["Phone Number"])
        parsed_number = phonenumbers.parse(phone_number, "US")  # Assuming the number is from the US
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        # Customize the message
        message_body = f"Hi {name}, this is a quick reminder for our upcoming event! Let us know if you have questions."

        try:
            # Send SMS
            message = textClient.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=formatted_number
            )
            print(f"Sent message to {name} at {phone_number}")
        except Exception as e:
            print(f"Failed to send message to {name} at {phone_number}: {e}")

# Run the function
send_personalized_texts()

creds = Credentials.from_service_account_file('creds.json', scopes=scopes)
sheetClient = gspread.authorize(creds)
# Update google sheets
sheet = sheetClient.open("Test spreadsheet").sheet1

# Update a specific cell
sheet.update([["Hello, Google Sheets!"]], "A6")
