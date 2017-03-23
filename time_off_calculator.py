#!/usr/bin/env python
"""Helper script to compute Time off for an employee using data from google sheets.
@author: aravind

Based on tutorial at :
https://developers.google.com/sheets/api/quickstart/python

Requires google-api-python-client
pip install --upgrade google-api-python-client
"""


from datetime import date
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SICK_HOURS=64
VACATION_HOURS=96
START_DATE=date(2016,5,16)
VACATION_PER_WEEK=VACATION_HOURS*1.0/52
SICK_PER_WEEK=SICK_HOURS*1.0/52

SCOPES="https://www.googleapis.com/auth/spreadsheets.readonly"
SPREADSHEET_ID="1gc5oMQLM1NX8WdVcQR2TtRWbpJeuRpAEW-U4bQspHao"
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME="Time Off Calculator"
def hours_used(data):
    vacation_total=0
    sick_total=0
    for row in data:
        if row[2].lower()=="sick":
            sick_total+=float(row[1])
        if row[2].lower()=="vacation":
            vacation_total+=float(row[1])
    return vacation_total,sick_total

def hours_eligible(as_of_date=date.today()):
    worked_weeks=(as_of_date-START_DATE).days/7
    vacation_hours_eligible=worked_weeks*VACATION_PER_WEEK
    sick_hours_eligible=worked_weeks*SICK_PER_WEEK
    return vacation_hours_eligible,sick_hours_eligible

def time_off_stats(data):
    vacation_hours_eligible,sick_hours_eligible=hours_eligible()
    vacation_hours_used,sick_hours_used=hours_used(data)

    print("Vacation Total Hours per Year",VACATION_HOURS)
    print("Vacation Total Hours per Week",VACATION_PER_WEEK)
    print("Vacation Hours Used",vacation_hours_used)
    print("Vacation Hours Eligible",vacation_hours_eligible)
    print("Vacation Hours Balance",vacation_hours_eligible-vacation_hours_used)

    print("Sick Total Hours per Year",SICK_HOURS)
    print("Sick Total Hours per Week",SICK_PER_WEEK)
    print("Sick Hours Used",sick_hours_used)
    print("Sick Hours Eligible",sick_hours_eligible)
    print("Sick Hours Balance",sick_hours_eligible-sick_hours_used)


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'time_off_calculator.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow=client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags=None)
    return credentials

def get_data(credentials,spreadsheetId=SPREADSHEET_ID,rangeName="data!A2:E1000"):
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    return values

if __name__=="__main__":
    credentials=get_credentials()
    data=get_data(credentials)
    time_off_stats(data)
