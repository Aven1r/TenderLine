import base64
import os

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



TOKEN_DATA = {'access_token': 'ya29.a0AfB_byAgOb8NzJZdyIXW8Av9wJpOTv7TGshQyOgP4gEEQt_-PWTaLIG2ymPu7e17HUF32yG32cYs_-DFUMIS78GObaQbqU69hSgQpWvZYJ7J8ogSPCrEuCFFQEI6KRyG6w60p5pmcVNXzakRy665HtuYh82m0teJsyDLaCgYKAdQSARASFQHGX2Mit_rsCojKaTt-8RsiPViMMg0171', 
              'expires_in': 3599, 
              'refresh_token': '1//09PoS-nkxzNboCgYIARAAGAkSNwF-L9IrnOj80M_qrvRbEsBpXwQzQ0kencqdXjOmVTyo3piGFHn-I7Y1v0PsGcNj7I7iVXYkIYc', 
              'scope': 'https://www.googleapis.com/auth/gmail.send', 
              'token_type': 'Bearer',
              "client_secret": "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",
              "client_id": "51270546914-gu442nra818l7ur1jc1pj0cbgh6vtotu.apps.googleusercontent.com"}

def send_pdf(email_info, attachment):
  # Build the Gmail service
  creds = Credentials.from_authorized_user_info(TOKEN_DATA)
  service = build('gmail', 'v1', credentials=creds)
  attachment = os.path.abspath('backend/api/documents/generated/contract.pdf')

  # Refresh the token if it's expired
  if creds.expired:
        creds.refresh(Request())

  # Create the email message
  email = MIMEMultipart()
  email['to'] = email_info
  email['subject'] = 'TenderLine: файл контракта по закупке Елочных украшений'
  email.attach(MIMEText('Готовый файл договора во вложении'))

  # Add the attachment
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(open(attachment, 'rb').read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
  email.attach(part)

  # Send the email
  raw_message = {'raw': base64.urlsafe_b64encode(email.as_bytes()).decode('utf-8')}
  try:
    message = service.users().messages().send(userId='me', body=raw_message).execute()
    print('Email sent successfully!')
  except HttpError as error:
    print(f'An error occurred: {error}')


def notify_user(email, contract_number):
   # Build the Gmail service
  creds = Credentials.from_authorized_user_info(TOKEN_DATA)
  service = build('gmail', 'v1', credentials=creds)

  # Refresh the token if it's expired
  if creds.expired:
        creds.refresh(Request())

  # Create the email message
  email = MIMEText(f'Новое сообщение в контракте {contract_number}')
  email['to'] = email
  email['subject'] = 'TenderLine: Новое сообщение'

  # Send the email
  raw_message = {'raw': base64.urlsafe_b64encode(email.as_bytes()).decode('utf-8')}
  try:
    message = service.users().messages().send(userId='me', body=raw_message).execute()
    print('Email sent successfully!')
  except HttpError as error:
    print(f'An error occurred: {error}')
