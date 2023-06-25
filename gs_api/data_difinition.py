from googleapiclient.discovery import build

from .file_utils import FileUtils
class DataDefinition:
    def __init__(self):
        self.service = None
        self.__authenticate()

    def __enter__(self):
        self.user_tables = FileUtils.load_user_tables()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        FileUtils.save_user_tables(self.user_tables)

    def __authenticate(self):
        creds = FileUtils.load_credentials()
        self.service = build('sheets', 'v4', credentials=creds)

    def get_table_id_by_name(self, table_name: str) -> str or None:
        for table in self.user_tables:
            for id, name in table.items():
                if name == table_name:
                    return id
        return None

    def create_table(self, title: str, column_names: list[str], column_color: [int, int, int] = None) -> dict:
        if column_color is None:
            column_color = [70, 69, 68]

        if self.get_table_id_by_name(title):
            raise Exception(f"Table named {title} already exists!")

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

        self.user_tables.append({result['spreadsheetId']: title})

        return result

    def update_table(self, title: str, new_title: str, new_column_names: list[str] = None) -> dict:
        table_id = self.get_table_id_by_name(title)

        if not table_id:
            raise Exception(f"Table named {title} not found!")

        if new_column_names is None:
            new_column_names = self.service.spreadsheets().values().get(spreadsheetId=table_id, range='A1:1').execute().get('values')[0]

        if self.get_table_id_by_name(new_title):
            raise Exception(f"Table named {title} already exists!")

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
            raise Exception("The number of new column names exceeds the number of columns in the table.")

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

    def delete_table(self, title: str):
        table_id = self.get_table_id_by_name(title)

        if not table_id:
            raise Exception(f"Table named {title} not found!")

        # TODO: Нельзя удалить всю таблицу (только листы), хз чё делать

        for table in self.user_tables:
            if table.get(table_id):
                del table[table_id]
                break