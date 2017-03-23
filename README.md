##time_off_calculator
Time Off Calculator(time_of_calculator.py) is a simple python utility to Keep track of time off of your part-time employee using google spreadsheets


###Installation
Check out https://developers.google.com/sheets/api/quickstart/python contains information for prerequirements and setup


###Usage
Configure the following in the top of the script:

SICK_HOURS
VACATION_HOURS
START_DATE#date
VACATION_PER_WEEK
SICK_PER_WEEK=

SCOPES="https://www.googleapis.com/auth/spreadsheets.readonly"
SPREADSHEET_ID="1gc5oMQLM1NX8WdVcQR2TtRWbpJeuRpAEW-U4bQspHao"
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME="Time Off Calculator"

Execution: python time_off_calculator.py
