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
sheet = sheetClient.open("Public invite").sheet1
expected_headers = ['What is your name?', 'Formatted Phone Number']
data = sheet.get_all_records(expected_headers=expected_headers )
contacts_df = pd.DataFrame(data)

# Function to send personalized messages
def send_personalized_texts():
    for index, row in contacts_df.iterrows():
        name = row['What is your name?']
        print(row["Formatted Phone Number"])
        phone_number = "+1"+str(row["Formatted Phone Number"])
        parsed_number = phonenumbers.parse(phone_number, "US")  # Assuming the number is from the US
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        # Customize the message
        message_body = f"Hey {name.split()[0]}! This is the Jacksonville Palestine Solidarity Network, and we're inviting you to our free screening of the film \"Tell Your Tale, Little Bird\", a documentary by Arab Loutfi that highlights revolutionary Palestinian women.\n \nThe screening will be this Saturday (3/15) hosted at Falafel X Bar (4162 Herschel St.). Doors will open at 6:30PM, we'll start the film at 7PM, and there will be a food & prayer intermission from 7:30-8PM\n \n For those participating in Ramadan, we encourage you to call ahead the same day and make a note for your order to be ready at 7:30PM to break your fast on time. \n \nSee you there!"
        
        # Skip if phone number is null or NaN
        if pd.isna(phone_number) or phone_number == "":
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
            print(f"Sent message to {name} at {phone_number}")
        except Exception as e:
            print(f"Failed to send message to {name} at {phone_number}: {e}")

# Run the function
# UNCOMMENT BELOW TO SEND TEXTS
send_personalized_texts() 

# Read all values from column A (you can specify any column)
column_values = sheet.col_values(3)  # Column index starts at 1 for 'A', 3 for 'C'

# Increment numeric values
updated_values = []
for value in column_values:
    try:
        # Convert to int, increment, and add to the updated list
        updated_values.append([int(value) + 1])
    except ValueError:
        # Handle non-numeric values (keep them unchanged or handle differently)
        updated_values.append([value])

# Update the column with new values
range_to_update = f"C1:C{len(updated_values)}"  # Define the range
sheet.update(range_name=range_to_update, values=updated_values)

# Highlight color based on text count
# yellow = 1x contact attempt (col C), not JPSN member (col D)
# orange = 2x contact attempt (col C), not JPSN member (col D)
# green = JPSN member (col D)
    # POSSIBLE NEW FEATURE: move to different tab for JPSN members and remove from current sheet 
# POSSIBLE NEW FEATURE: 3+ contact attempts && not JPSN member => archive number in a different tab and remove from current sheet

# POSSIBLE NEW FEATURE: be able to send messages depending on membership status
# ex: can send out texts for non JPSN members for general event reminders,
#       and reminders for JPSN members for organization specific matters

# Get the total number of rows with data
rows_with_data = len(updated_values)

# Loop through each row and check conditions to apply colors
for row in range(2, rows_with_data + 1):  # Skip header row, start from 2
    contact_attempts = sheet.cell(row, 3).value  # Column C (Contact Attempts)
    member_status = sheet.cell(row, 4).value  # Column D (Member Status)
    
    if member_status == "Yes":
        # Green color for JPSN members
        color = {'red': 0, 'green': 1, 'blue': 0}
    elif contact_attempts == '1':
        # Yellow for 1x contact attempt, not a JPSN member
        color = {'red': 1, 'green': 1, 'blue': 0}
    elif contact_attempts == '2':
        # Orange for 2x contact attempt, not a JPSN member
        color = {'red': 1, 'green': 0.6, 'blue': 0}
    else:
        continue  # No coloring if the conditions are not met

    # Update the background color for columns A to D in the current row
    range_to_update = f"A{row}:D{row}"
    sheet.format(range_to_update, {'backgroundColor': color})