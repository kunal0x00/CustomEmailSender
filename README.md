# CustomEmailSender

This script is designed to automate the process of sending personalized emails. It replaces placeholders in your email draft with specific inputs you provide, allowing you to easily customize messages for different recipients.

## Features

- **Placeholder Replacement:** Replace placeholder text like `<enter company name>` in your email draft with actual values you provide.
- **Multiple Recipients:** Send personalized emails to multiple recipients simultaneously.
- **Multiple Attachments:** Attach multiple PDF files to your emails.

## How It Works

1. **Prepare Your Email Draft:** Create a draft email with placeholders for dynamic content.
2. **Provide Recipient Details:** Enter the email addresses of recipients and the company name or other specific details.
3. **Attach Files:** Optionally, attach multiple PDF files to your emails.
4. **Send Emails:** The script sends the customized email to each recipient with the specified attachments.

This script is ideal for sending out personalized messages where certain details need to be tailored for each recipient.

## credentials.json File

The `credentials.json` file contains the OAuth 2.0 client secrets required for authenticating with Google APIs. This file is generated from the Google Cloud Console and includes essential information such as your client ID and client secret.

### Steps to Obtain `credentials.json`

1. **Go to the Google Cloud Console:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/).

2. **Create a Project:**
   - If you don’t already have a project, create a new project by clicking on the project dropdown and selecting "New Project."

3. **Enable the Gmail API:**
   - Go to the API Library and search for "Gmail API."
   - Click on "Enable" to enable the Gmail API for your project.

4. **Create OAuth 2.0 Credentials:**
   - Go to the Credentials page.
   - Click on "Create Credentials" and select "OAuth 2.0 Client ID."
   - Configure the OAuth consent screen if you haven't done so already.
   - Choose "Desktop app" as the application type (or another appropriate type based on your use case).
   - Provide a name for the client ID and click "Create."

5. **Download `credentials.json`:**
   - After creating the OAuth 2.0 client ID, you'll be able to download the `credentials.json` file.
   - Click on "Download" to save the file to your local machine.

### Content of `credentials.json`

The `credentials.json` file will look something like this:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [
      "urn:ietf:wg:oauth:2.0:oob",
      "http://localhost"
    ]
  }
}

### New Feature: Multiple Attachments

This script now supports sending multiple attachments, allowing you to specify a different file for each recipient.

- **Single Attachment:** If only one file is provided, it will be sent to all recipients.
- **Multiple Attachments:** If the number of files matches the number of email addresses, each email will receive the corresponding file. For example, if you send emails to three addresses and provide three files, each recipient will receive their respective file.

To use this feature, simply provide the paths to the files as a comma-separated list when prompted.

