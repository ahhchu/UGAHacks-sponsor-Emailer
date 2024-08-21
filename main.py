from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv  

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', scopes=['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send'])

    credentials = flow.run_local_server(port=8080)
    return build('gmail', 'v1', credentials=credentials)
def extract_csv():

    with open('cleaned.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            send_email(lines)

def send_email(line):
    print(line)
if __name__ == '__main__':
    try:
        service = get_service()
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])
    except Exception as e:
        print(f"An error occurred: {e}")

