from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
import pandas as pd
import time

# Constants
SENDER_EMAIL = 'nichebox.co@gmail.com' #make sure to use the same gmail as the sending email
CC_EMAILS = 'jnp00008@uga.edu, khushi.bhatamrekar@uga.edu, hemant.gautam@uga.edu'  # Add constant CC addresses here
EMAIL_TEMPLATE = '''<p>Dear {name},</p>
 
<p>I hope this message finds you well! My name is Catherine, and, along with two other students from the University of Georgia, I co-founded NicheBox, a startup focused on delivering unique team-building experiences through our carefully crafted hobby kits. Each NicheBox is designed to bring a fresh twist to corporate outings, encouraging creativity and connection within teams.</p>
 
<p>We’re excited to offer two versatile options that can elevate your next event: a Team Painting Kit for a collaborative and hands-on experience or a Digital Office Icebreaker Bundle that promotes team bonding in a fun and interactive way, ideal for remote or hybrid teams. Each kit is customizable to match your company's culture and goals, making it a memorable experience for everyone involved.</p>

<p>If you're interested in learning more or would like to explore a trial, we’d be thrilled to discuss how NicheBox can bring a unique and impactful touch to your team building events. Thank you for considering a partnership with us, and we look forward to the opportunity to work together!</p>

<p>Warm Regards,</p>

<p>Catherine Chu</p>
<strong>Co-Founder, NicheBox</strong><br>
<strong>University of Georgia</strong><br>
<strong>nichebox.co@gmail.com</strong></p>
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
        personalized_subject = f"NicheBox and {row['Company Name']} Partnership"
        email_body = EMAIL_TEMPLATE.format(name=row['First Name'], company_name=row['Company Name'])
        message = create_message(SENDER_EMAIL, row['Email'], personalized_subject, email_body)
        send_email(service, message)
        time.sleep(5)

if __name__ == '__main__':
    try:
        service = get_service()
        extract_and_send_emails(service)
    except Exception as e:
        print(f"An error occurred: {e}")
