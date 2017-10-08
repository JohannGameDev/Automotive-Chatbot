import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime


class Calendar(object):

    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Calendar API Python Quickstart'
        self.credentials = self.get_credentials()


    def get_credentials(self):
        """Gets valid user credentials from storage.


        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            print "You have to setup Credentials"
        return credentials

    def get_events(self):
            """

            Creates a Google Calendar API service object and outputs a list of the next
            10 events on the user's calendar.
            """

            http = self.credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)

            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            print 'Getting the upcoming 10 events'
            eventsResult = service.events().list(
                calendarId='primary', timeMin=now, maxResults=2, singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])

            if not events:
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                des = event.get("description",None)

                print(start, event['summary'],des)
            return events
