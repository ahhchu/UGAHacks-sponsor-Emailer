from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
import pandas as pd
import time

# Constants
SENDER_EMAIL = 'henry.lue@ugahacks.com' #make sure to use the same gmail as the sending email
CC_EMAILS = 'hello@ugahacks.com, sponsor@ugahacks.com'  # Add constant CC addresses here
EMAIL_TEMPLATE = '''<p>Dear {name},</p>
 
<p>My name is Henry and I am a sponsorship organizer for UGAHacks, the official student-run hackathon for the University of Georgia (UGA). Our event is a 3-day coding competition consisting of challenging programming contests, networking with top tech companies, and classes on new cutting-edge technologies pervading the market.</p>
 
<p>This upcoming February 7th-9th we are excited to hold our 10th annual Hackathon here at UGA! We believe that {company_name} would be a perfect asset for UGAHacks X. Support from our previous sponsors such as BlackRock, State Farm, and Capital One made our hackathons successful. This year is expected to be our biggest event yet, with an estimated attendance of 800 hackers. With {company_name} as an official sponsor, we could make this the most exciting and memorable event thus far.</p>

<p>UGAHacks X will be an incredible opportunity for {company_name}. Our partners have the chance to connect with our top participants by arranging their own competitions and events, introducing their technologies, reviewing student resumes, and hosting in-person interviews. UGAHacks’ participants come from all around the country, with some notable universities being UGA, Georgia Tech, NYU, and others.</p>

<p>I would love to send you our Sponsorship Packet and set up a meeting or call with you if you are interested in being involved with our 10th annual Hackathon!</p>
<p>If you have any questions, don’t hesitate to reach me via email. Thank you for your time, and we look forward to hearing from you!</p>

<p>Best,</p>

<p>Henry Lue</p>
<strong>Sponsorship Team</strong><br>
<strong>UGAHacks X</strong></p>
'''

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
    credentials = flow.run_local_server(port=8080)
    return build('gmail', 'v1', credentials=credentials)

def create_message(sender, to, subject, message_text, cc=CC_EMAILS):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc:
        message['cc'] = cc  # Set CC field
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def send_email(service, message):
    try:
        message = service.users().messages().send(userId='me', body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def extract_and_send_emails(service):
    df = pd.read_csv('data/batch.csv')
    for index, row in df.iterrows():
        personalized_subject = f"UGA Hacks and {row['Company Name for Emails']} Partnership"
        email_body = EMAIL_TEMPLATE.format(name=row['First Name'], company_name=row['Company Name for Emails'])
        message = create_message(SENDER_EMAIL, row['Email'], personalized_subject, email_body)
        send_email(service, message)
        time.sleep(5)

if __name__ == '__main__':
    try:
        service = get_service()
        extract_and_send_emails(service)
    except Exception as e:
        print(f"An error occurred: {e}")
