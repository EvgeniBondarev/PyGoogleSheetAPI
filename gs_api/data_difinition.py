import os.path
import pickle
import json
import csv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .Exceptions import TableValueOverflow, TableNameUniqueness, TableNotFound


def get_file_path(file_path: str) -> str:
    directory = os.path.dirname(file_path)
    if not directory:
        return ''
    else:
        return directory

class DataDifinition():
    def __init__(self, credentials_file: str):
        self.SCOPES: list[str] = ['https://www.googleapis.com/auth/spreadsheets']
        self.service = None

        self.base_directory = get_file_path(credentials_file)
        self.__authenticate(credentials_file)

    def __enter__(self):
        self.__get_user_tables()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save_user_tables()


    def __authenticate(self, credentials_file: str):
        creds = None
        token_path = self.base_directory + "//token.pickle"
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def __get_user_tables(self):
        user_tables_path = self.base_directory + '//tables.json'

        if not os.path.exists(user_tables_path):
            self.user_tables = []
            return

        with open(user_tables_path, 'r') as file:
            tables = json.load(file)

        self.user_tables = tables

    def __save_user_tables(self):
        user_tables_path = self.base_directory + '//tables.json'

        with open(user_tables_path, 'w') as file:
            json.dump(self.user_tables, file)

    def get_table_id_by_name(self, table_name):
        for table in self.user_tables:
            for id, name in table.items():
                if name == table_name:
                    return id
        return None

    def create_table(self, title, column_names, column_color=None):
        if column_color is None:
            column_color = [70, 69, 68]

        if self.get_table_id_by_name(title):
            raise TableNameUniqueness(f"Table named {title} already exists!")

        request_body = {
            'properties': {
                'title': title
            },
            'sheets': [
                {
                    'properties': {
                        'sheetId': 0,
                        'title': title,
                        'gridProperties': {
                            'columnCount': len(column_names),
                            'frozenRowCount': 1
                        }
                    },
                    'data': [
                        {
                            'startRow': 0,
                            'startColumn': 0,
                            'rowData': [
                                {
                                    'values': [
                                        {
                                            'userEnteredValue': {
                                                'stringValue': name
                                            },
                                            'userEnteredFormat': {
                                                'backgroundColor': {
                                                    'red': column_color[0],
                                                    'green': column_color[1],
                                                    'blue': column_color[2]
                                                },
                                            }
                                        } for name in column_names
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        result = self.service.spreadsheets().create(body=request_body).execute()

        self.user_tables.append({result['spreadsheetId']:title})
        return result

    def update_table(self, title, new_title, new_column_names=None):
        table_id = self.get_table_id_by_name(title)

        if not table_id:
            raise TableNotFound(f"Table named {title} not found!")

        if new_column_names is None:
            new_column_names = self.service.spreadsheets().values().get(spreadsheetId=table_id, range='A1:1').execute().get('values')[0]
            print(new_column_names)


        if self.get_table_id_by_name(new_title):
            raise TableNameUniqueness(f"Table named {title} already exists!")

        spreadsheet = self.service.spreadsheets().get(spreadsheetId=table_id).execute()
        sheet_properties = spreadsheet['sheets'][0]['properties']
        column_count = sheet_properties['gridProperties']['columnCount']

        request_body = {
            'requests': [
                {
                    'updateSpreadsheetProperties': {
                        'properties': {
                            'title': new_title
                        },
                        'fields': 'title'
                    }
                }
            ]
        }

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=table_id,
            body=request_body
        ).execute()

        if len(new_column_names) > column_count:
            raise TableValueOverflow("The number of new column names exceeds the number of columns in the table.")
        request_body = {
            'requests': [
                {
                    'updateCells': {
                        'start': {
                            'sheetId': sheet_properties['sheetId'],
                            'rowIndex': 0,
                            'columnIndex': 0
                        },
                        'rows': [
                            {
                                'values': [
                                    {
                                        'userEnteredValue': {
                                            'stringValue': name
                                        }
                                    } for name in new_column_names
                                ]
                            }
                        ],
                        'fields': 'userEnteredValue'
                    }
                }
            ]
        }

        result = self.service.spreadsheets().batchUpdate(
            spreadsheetId=table_id,
            body=request_body
        ).execute()

        for table in self.user_tables:
            if table.get(table_id):
                table[table_id] = new_title
                break

        return result

    def delete_table(self, title):
        table_id = self.get_table_id_by_name(title)

        if not table_id:
            raise TableNotFound(f"Table named {title} not found!")

        # TODO: Нельзя удалить всю таблицу (только листы), хз чё делать

        for table in self.user_tables:
            if table.get(table_id):
                del table[table_id]
                break

    def download_table(self, save_folder, title):
        table_id = self.get_table_id_by_name(title)

        if not table_id:
            raise TableNotFound(f"Table named {title} not found!")

        file_path = os.path.join(save_folder, f"{title}.csv")

        response = self.service.spreadsheets().values().get(
            spreadsheetId=table_id,
            range='A1:ZZ'
        ).execute()

        values = response.get('values', [])
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(values)









