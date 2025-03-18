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
creds = Credentials.from_service_account_file('creds.json', scopes=scopes)
sheetClient = gspread.authorize(creds)

# Update google sheets
sheet = sheetClient.open("2-21-phonebanking-public-invite").sheet1
expected_headers = ['From','To', 'Body', 'categories']
data = sheet.get_all_records(expected_headers=expected_headers )
contacts_df = pd.DataFrame(data)

# Function to send personalized messages
def send_personalized_texts():
    for index, row in contacts_df.iterrows():
        # name = row['What is your name?']
        print(row["To"])
        status = row["categories"]
        phone_number = str(row["To"])
        parsed_number = phonenumbers.parse(phone_number, "US")  # Assuming the number is from the US
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        # Customize the message
        message_body = row['Body']       

        # Skip if phone number is null or NaN
        if pd.isna(phone_number) or phone_number == "" or status != "failed":
            # print(f"Failed to send to {name}: Phone number is null or empty.")
            print(f"Failed to send: Phone number is null or empty.")
            continue

        try:
            # Send SMS
            message = textClient.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=formatted_number
            )
            print(f"Sent message to  {phone_number}")
        except Exception as e:
            print(f"Failed to send message to {phone_number}: {e}")

# Run the function
# UNCOMMENT BELOW TO SEND TEXTS
send_personalized_texts() 

