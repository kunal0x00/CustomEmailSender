import base64
import pickle
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from googleapiclient.discovery import build

def send_email(service, sender_email, receiver_emails, subject, body, attachment_paths=None):
    for receiver_email in receiver_emails:
        # Create a MIME multipart message for each recipient
        message = MIMEMultipart()
        message['to'] = receiver_email
        message['from'] = sender_email
        message['subject'] = subject

        # Attach the email body
        message.attach(MIMEText(body, 'plain'))

        # Attach the PDF files if provided
        if attachment_paths:
            for attachment_path in attachment_paths:
                if os.path.isfile(attachment_path):
                    with open(attachment_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                        message.attach(part)

        # Encode the message and send it
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        raw_message = {'raw': raw}

        try:
            response = service.users().messages().send(userId='me', body=raw_message).execute()
            print(f'Email sent to {receiver_email}. Message Id: {response["id"]}')
        except Exception as e:
            print(f'An error occurred while sending to {receiver_email}: {e}')

def main():
    # Load the credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        service = build('gmail', 'v1', credentials=creds)

        # Get user inputs
        email_draft_path = input("Enter the path to the email draft file: ")
        if not os.path.isfile(email_draft_path):
            print(f"Error: File {email_draft_path} not found.")
            return

        receiver_emails = input("Enter the receiver's email addresses (comma-separated): ").split(',')
        receiver_emails = [email.strip() for email in receiver_emails]

        company_name = input("Enter the company name: ")

        attachment_paths_input = input("Enter the paths to the PDF files you want to attach (comma-separated, or leave blank if none): ")
        attachment_paths = [path.strip() for path in attachment_paths_input.split(',')] if attachment_paths_input else None

        # Read the email draft from the file
        with open(email_draft_path, 'r') as file:
            draft_mail = file.read()

        # Validate inputs
        if not receiver_emails:
            print("Error: At least one receiver's email address is required.")
            return

        # Replace placeholder and send the email
        email_body = draft_mail.replace("<enter company name>", company_name)
        send_email(service, "yourEmail@gmail.com", receiver_emails, f"Application for Internship at {company_name}", email_body, attachment_paths)
    else:
        print("Token not found. Please run the authentication script first.")

if __name__ == "__main__":
    main()
