#!/usr/bin/env python
# coding:utf-8
"""
Name    : Calendar.py
Author  : Ashley_SEBBAG
Contact : ashsebbag@gmail.com
Time    : 27/03/2021 12:32
Desc    :
"""
from __future__ import print_function
import pandas as pd
import DB as db
import config as cfg
from datetime import datetime, timedelta
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


data = db.Database()
nb_event = 1
sql = f"SELECT * FROM Events LIMIT {nb_event}"
df = pd.read_sql(sql, data.con)

timestamp = int(df['times'].to_list()[0][:-3])
date = datetime.fromtimestamp(timestamp)
start_datetime = date.strftime('%Y-%m-%dT%H:%M:%S')
end_datetime = (date + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', cfg.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', cfg.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    add_event = True

    for event in events:
        if event['summary'] == df['title'].to_list()[0]:
            add_event = False

    if add_event:
        event = {
            'summary': df['title'].to_list()[0],
            'location': df['address'].to_list()[0],
            "organizer": {
                "displayName": df['host'].to_list()[0],
                "self": True
            },
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Asia/Jerusalem',
            },
            'end': {
                'dateTime':  end_datetime,
                'timeZone': 'Asia/Jerusalem',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
        }

        service.events().insert(calendarId='primary', body=event).execute()


if __name__ == '__main__':
    main()
