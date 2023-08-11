from __future__ import print_function
import os
import base64
import re
import os.path
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_2fa_code_from_gmail(subject):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

   
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    # Retrieve the list of unread messages
     # Get today's date
    today = datetime.now().strftime('%Y/%m/%d')

    # Construct the query for emails from today
    query = f'after:{today}'

    # Retrieve the list of unread messages matching the query
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found.')
        return None

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        msg_data = msg['payload']['headers']
        sender = next((header['value'] for header in msg_data if header['name'] == 'From'), None)
        message_subject = next((header['value'] for header in msg_data if header['name'] == 'Subject'), None)

        if message_subject and subject in message_subject:
            if 'parts' in msg['payload']:
                parts = msg['payload']['parts']
                for part in parts:
                    if part['mimeType'] == 'text/html':  # Check for HTML content
                        body = part['body']
                        if 'data' in body:
                            data = body['data']
                            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')

                            # Find code after "code is" with possible capitalization variations
                            code = re.search(r'(?i)code is\s+(\d{6})', decoded_data)
                            if code:
                                return code.group(1)
            elif 'body' in msg['payload']:
                body = msg['payload']['body']
                if 'data' in body:
                    data = body['data']
                    decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                    code = re.search(r'(?i)code is\s+(\d{6})', decoded_data)
                    if code:
                        return code.group(1)

    # No matching email found
    print(f'No 2-factor code found with "{subject}" subject.')
    return None