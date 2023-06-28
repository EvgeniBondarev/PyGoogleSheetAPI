import os
import json
import pickle
from .Exceptions import *

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CREDENTIALS = ''

def authorization(credentials: str):
    global CREDENTIALS
    CREDENTIALS = credentials

class FileUtils:
    @staticmethod
    def get_file_path(filename: str) -> str:
        return os.path.dirname(os.path.abspath(filename))

    @staticmethod
    def load_credentials():
        creds = None
        token_path = os.path.join(FileUtils.get_file_path(CREDENTIALS), "token.pickle")

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS, ['https://www.googleapis.com/auth/spreadsheets'])
                creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    @staticmethod
    def load_user_tables():
        user_tables_path = os.path.join(FileUtils.get_file_path(CREDENTIALS), 'tables.json')

        if not os.path.exists(user_tables_path):
            return []

        with open(user_tables_path, 'r') as file:
            tables = json.load(file)

        return tables

    @staticmethod
    def save_user_tables(tables):
        user_tables_path = os.path.join(FileUtils.get_file_path(CREDENTIALS), 'tables.json')

        with open(user_tables_path, 'w') as file:
            json.dump(tables, file)
    @staticmethod
    def get_table_id_by_name(table_name: str) -> str or None:
        user_tables = FileUtils.load_user_tables()
        for table in user_tables:
            for id, name in table.items():
                if name == table_name:
                    return id

        raise TableNotFound(table_name)
    @staticmethod
    def get_table_name_by_id(service, table_id: str) -> str:
        spreadsheet = service.spreadsheets().get(spreadsheetId=table_id).execute()
        table_name = spreadsheet['properties']['title']
        return table_name
