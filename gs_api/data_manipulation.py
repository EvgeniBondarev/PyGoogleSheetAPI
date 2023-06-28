from googleapiclient.discovery import build
import pandas as pd
import pandasql as ps

from .file_utils import FileUtils


class DataManipulation:
    def __init__(self):
        self.service = None
        self.__authenticate()

        self.table_id = None
        self.table_name = None


    def __authenticate(self):
        creds = FileUtils.load_credentials()
        self.service = build('sheets', 'v4', credentials=creds)

    def connect(self, table_data):
        table_id = FileUtils.get_table_id_by_name(table_data)
        if table_id:
            self.table_name = table_data
            self.table_id = table_id
        else:
            self.table_name = FileUtils.get_table_name_by_id(self.service, table_data)
            self.table_id = table_data

        return (self.table_id, self.table_name)

    def insert(self, data):
        range_ = self.table_name
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.table_id).execute()
        sheet_properties = spreadsheet['sheets'][0]['properties']
        column_count = sheet_properties['gridProperties']['columnCount']

        # Проверяем количество столбцов в таблице
        if len(data[0]) > column_count:
            print('Ошибка: Количество значений превышает количество столбцов в таблице.')
            return

        value_range_body = {
            'values': data
        }

        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.table_id,
            range=range_,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=value_range_body
        ).execute()

        return result

    def read_all_data_from_sheet(self, title):
        table_id = FileUtils.get_table_id_by_name(title)

        if not table_id:
            raise Exception(f"Table named {title} not found!")

        result = self.service.spreadsheets().values().get(
            spreadsheetId=table_id,
            range=title
        ).execute()

        return result.get('values', [])

    def select_data(self, title, sql_query):
        data = self.read_all_data_from_sheet(title)
        columns = data[0]
        data.pop(0)


        df = pd.DataFrame(data, columns=columns)
        new_sql = sql_query.replace(f" {title} ", f" {df} ")

        print(sql_query)
        print(new_sql)

        result = ps.sqldf(new_sql, locals())


        return result