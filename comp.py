import base64
import pickle
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from googleapiclient.discovery import build

def send_email(service, sender_email, receiver_email, subject, body, attachment_path=None):
    # Create a MIME multipart message for each recipient
    message = MIMEMultipart()
    message['to'] = receiver_email
    message['from'] = sender_email
    message['subject'] = subject

    # Attach the email body
    message.attach(MIMEText(body, 'plain'))

    # Attach the file if provided
    if attachment_path:
        print(f"Attaching file: {attachment_path} to {receiver_email}")
        if os.path.isfile(attachment_path):
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                message.attach(part)
        else:
            print(f"Error: File {attachment_path} not found.")
            return

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

        placeholders = input("Enter the placeholders (comma-separated, corresponding to each email): ").split(',')

        attachment_paths_input = input("Enter the paths to the files you want to attach (comma-separated, or leave blank if none): ")
        attachment_paths = [path.strip() for path in attachment_paths_input.split(',')] if attachment_paths_input else None

        # Read the email draft from the file
        with open(email_draft_path, 'r') as file:
            draft_mail = file.read()

        # Validate inputs
        if not receiver_emails:
            print("Error: At least one receiver's email address is required.")
            return

        if len(placeholders) == 1:
            placeholders = placeholders * len(receiver_emails)

        if len(placeholders) != len(receiver_emails):
            print("Error: The number of placeholders must match the number of email addresses or be exactly one.")
            return

        if attachment_paths and len(attachment_paths) != 1 and len(attachment_paths) != len(receiver_emails):
            print(f"Error: The number of attachment paths ({len(attachment_paths)}) must be either 1 or match the number of email addresses ({len(receiver_emails)}).")
            return

        # Replace placeholder and send the email
        for i, receiver_email in enumerate(receiver_emails):
            email_body = draft_mail.replace("<enter company name>", placeholders[i])
            attachment_path = attachment_paths[i] if attachment_paths and len(attachment_paths) > 1 else attachment_paths[0] if attachment_paths else None
            print(f"Sending email to: {receiver_email} with placeholder: {placeholders[i]} and attachment: {attachment_path}")
            send_email(service, "yourEmail@gmail.com", receiver_email, f"Application for Internship at {placeholders[i]}", email_body, attachment_path)#this line is for Subject of email, no need to change the yourEmail@gmail.com
    else:
        print("Token not found. Please run the authentication script first.")

if __name__ == "__main__":
    main()
