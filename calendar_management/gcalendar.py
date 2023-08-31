import datetime
import os.path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from calendar_management.mailing import get_emails_list

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def gcalendar_service():
    creds = None
    if os.path.exists(os.getenv('token')):
        creds = Credentials.from_authorized_user_file(os.getenv('token'), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('creds'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service


def parse_event_info(event_info):
    event_date = datetime.strptime(event_info['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
    event_time = datetime.strptime(event_info['time'], '%H:%M').strftime('%H:%M:%S')
    return event_date, event_time


def send_event_to_calendar(event_info, service):
    event_date, event_time = parse_event_info(event_info)
    start_time = event_time
    event_time = datetime.strptime(event_time, '%H:%M:%S')
    event_time += timedelta(minutes=50)
    end_time = event_time.strftime('%H:%M:%S')
    event = {
        'summary': event_info['title'],
        'location': event_info['location'],
        'start': {
            'dateTime': f"{event_date}T{start_time}",
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': f"{event_date}T{end_time}",
            'timeZone': 'Europe/Madrid',
        },
        'attendees': get_emails_list(),
        'sendNotifications': True,
    }
    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    return event