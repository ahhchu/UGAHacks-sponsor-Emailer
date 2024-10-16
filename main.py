from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
import pandas as pd
import time
from google.auth.exceptions import RefreshError

# Constants
SENDER_EMAIL = 'nichebox.co@gmail.com' #make sure to use the same gmail as the sending email
CC_EMAILS = 'jiya.patel@uga.edu'  # Add constant CC addresses here
EMAIL_TEMPLATE = '''<p>Dear {name},</p>
 
<p> Are you finding it challenging to plan a team building event? Organizing activities that align with your team’s goals, 
culture, and interests can be a tough task, and it often requires more time and effort than anticipated. {personal}</p>

<p> Let us take that responsibility off your plate. From selecting the right activities to managing every detail, 
we handle everything to ensure your team gets a meaningful, fun, and impactful event.</p>

<p>If you’d like to explore how we can create a hassle free, engaging experience for your team, let’s set up a time to chat!</p>

<p>Looking forward to the opportunity,</p>

<p>Khushi Bhatamrekar </p>
<strong>Co-Founder, Nichebox</strong><br>
<strong>nichebox.co@gmail.com</strong></p>
'''

def get_service():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
        credentials = flow.run_local_server(port=0)
        return build('gmail', 'v1', credentials=credentials)
    except RefreshError as e:
        print(f"RefreshError: {e}")
        print("This error often occurs when the client_secrets.json file is outdated or misconfigured.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

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
    df = pd.read_csv('data/test2_save_2024-10-15-1337.csv')
    
    for index, row in df.iterrows():
        personalized_subject = f"Need a Stress Free Solution for Your Next Team Building Event?"
        email_body = EMAIL_TEMPLATE.format(name=row['First Name'], company_name=row['Company Name'], personal=row['Personal'])
        message = create_message(SENDER_EMAIL, row['Email'], personalized_subject, email_body)
        send_email(service, message)
        time.sleep(5)

if __name__ == '__main__':
    try:
        service = get_service()
        if service:
            extract_and_send_emails(service)
        else:
            print("Failed to obtain Gmail service. Please check the error messages above.")
    except Exception as e:
        print(f"An error occurred: {e}")
