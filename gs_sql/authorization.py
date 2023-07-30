import os
import json
import pickle
from .Exceptions import *

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_file_path(filename: str) -> str:
        return os.path.dirname(os.path.abspath(filename))

def authenticate(credentials):
    creds = None
    token_path = os.path.join(get_file_path(credentials), "token.pickle")

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, ['https://www.googleapis.com/auth/spreadsheets'])
            creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service

