import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# The scope for sending emails via Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_google():
    creds = None
    # Load credentials from token.pickle, if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            print("Token loaded successfully.")
    # If there are no (valid) credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Token refreshed successfully.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("New token generated successfully.")
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print("Token saved successfully.")
    return creds

# Run the authentication process
authenticate_google()
print("Authentication successful. Tokens have been saved.")
