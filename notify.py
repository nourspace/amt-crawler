import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slackclient import SlackClient

G_SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

try:
    service_account = os.environ.get('GOOGLE_SERVICE_ACCOUNT_CREDS', '')
    service_account_dict = json.loads(service_account)
    google_credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_dict, G_SCOPES)
except ValueError:
    google_credentials = None

slack_token = os.environ.get('SLACK_API_TOKEN')


def update_worksheet(name, values):
    if not google_credentials:
        return
    google_client = gspread.authorize(google_credentials)
    worksheet = google_client.open(name).sheet1
    worksheet.append_row(values)


def post_to_slack(channel, message):
    if not slack_token:
        return
    slack_client = SlackClient(slack_token)
    slack_client.api_call('chat.postMessage', channel=channel, text=message)
