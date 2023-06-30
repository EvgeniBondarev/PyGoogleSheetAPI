from googleapiclient.discovery import build
import pandas as pd
import pandasql as ps

from .Exceptions import *
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


    def read_all_data_from_sheet(self, title):
        table_id = FileUtils.get_table_id_by_name(title)

        if not table_id:
            raise TableNotFound(title)

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

        new_query = sql_query.replace(title, "df", 1)

        result = ps.sqldf(new_query)


        return self.__dataframe_to_value(result)

    def __dataframe_to_value(self, dataframe):
        dataframe_len = len(dataframe.values.tolist())
        if dataframe_len > 1:
            return dataframe.values.tolist()

        if dataframe_len == 1:
            if len(dataframe.values.tolist()[0]) > 1:
                return dataframe.values.tolist()[0]
            else:
                return dataframe.values.tolist()[0][0]

    def insert_data(self, title, data, columns=None):
        table_id = FileUtils.get_table_id_by_name(title)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=table_id,
            range=title
        ).execute()

        values = result.get('values', [])

        if not values:
            raise TableEmpty(title)

        if columns is None:
            columns = values[0]
        else:
            if len(columns) != len(data):
                raise NumberOfColumns(columns, values)

            for col_name in range(len(columns)):
                if columns[col_name] != values[0][col_name]:
                    raise InvalidColumnName(title, columns[col_name])


        value_dict = {}
        for i, column in enumerate(columns):
            value_dict[column] = data[i]

        column_order = values[0]

        values_to_insert = []
        for column in column_order:
            if column in value_dict:
                values_to_insert.append(value_dict[column])
            else:
                values_to_insert.append('')

        values = [values_to_insert]
        value_range_body = {
            'values': values
        }

        update_result = self.service.spreadsheets().values().append(
            spreadsheetId=table_id,
            range=title,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=value_range_body
        ).execute()

        return update_result






