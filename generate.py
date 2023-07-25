from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes required by your application
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Create an instance of the OAuth2 flow object
flow = InstalledAppFlow.from_client_secrets_file('token.json', scopes=SCOPES)

# Run the flow to obtain OAuth2 credentials
creds = flow.run_local_server(port=0)

# Save the credentials to a file
with open('token.json', 'w') as token_file:
    token_file.write(creds.to_json())

# Create an instance of the Credentials object from the saved token file
creds = Credentials.from_authorized_user_file('token.json', SCOPES)