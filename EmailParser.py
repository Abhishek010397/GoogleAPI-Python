from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.errors import HttpError
import email
from Bot import post_message

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            'credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    try:
        service = build('gmail', 'v1', http=creds.authorize(Http()))
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        emails = results.get('messages', [])
        for email in emails:
            messageheader = service.users().messages().get(userId='me', id=email['id'],format='full',metadataHeaders=None).execute()
            headers = messageheader["payload"]["headers"]
            subject = [i['value'] for i in headers if i["name"] == "Subject"]
            if subject == ['Your-Message-Topic]:
                msg = service.users().messages().get(userId='me', id=email['id']).execute()
                print(msg['snippet'])
                response = msg['snippet']
                post_message(response)
            else:
                exit(0)
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
