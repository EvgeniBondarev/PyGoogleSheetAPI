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

    def read_all_data_from_sheet(self, table_id, sql_query=None):
        range_ = self.table_name  # Название листа таблицы

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.table_id,
            range=range_
        ).execute()

        return result.get('values', [])

    def filter_data(self, sql_query, data):
        # Преобразование данных в DataFrame
        df = pd.DataFrame(data, columns=['Column1', 'Column122', 'Column312'])

        query = "SELECT * FROM df ORDER BY Column1 DESC"
        result = ps.sqldf(query)


        return result.values.tolist()