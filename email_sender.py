from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
import pandas as pd
import time

# Constants
SENDER_EMAIL = 'henry.lue@ugahacks.com'  # Sending email
CC_EMAILS = 'hello@ugahacks.com, sponsor@ugahacks.com'  # CC addresses
EMAIL_TEMPLATE = '''<p>Dear {name},</p>
<p>My name is Henry and I am a sponsorship organizer for UGAHacks...</p>
'''  # truncated for brevity

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
GOOGLE_CLIENT_SECRETS_FILE = 'client_secrets.json'


def get_flow(redirect_uri):
    """Create the OAuth2 flow with a given redirect URI."""
    flow = Flow.from_client_secrets_file(GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = redirect_uri
    return flow


def create_message(sender, to, subject, message_text, cc=CC_EMAILS):
    """Create an email message with the specified content."""
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc:
        message['cc'] = cc  # Set CC field
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}


def send_email(service, message):
    """Send an email using the Gmail API."""
    try:
        message = service.users().messages().send(userId='me', body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def extract_and_send_emails(service):
    """Extract emails from CSV and send personalized emails."""
    df = pd.read_csv('data/batch.csv')  # Make sure the CSV file is correctly placed

    for index, row in df.iterrows():
        personalized_subject = f"UGA Hacks and {row['Company Name']} Partnership"
        email_body = EMAIL_TEMPLATE.format(name=row['First Name'], company_name=row['Company Name'])
        message = create_message(SENDER_EMAIL, row['Email'], personalized_subject, email_body)
        send_email(service, message)
        time.sleep(5)


def credentials_to_dict(credentials):
    """Convert OAuth2 credentials to a dictionary."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }
