import pandas as pd
import pandasql as ps
from typing import List
from enum import Enum

from .Exceptions import *
from .BaseData import BaseData
from .dataclasses import Answer
from .configuration import RESPONSE_TYPE


class ResponseType(Enum):
    DataFrame = "DataFrame"
    List = "List"
    Value = "Value"
class DataManipulation(BaseData):

    def read_all_data_from_sheet(self, title):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.table_id,
            range=title
        ).execute()

        return result.get('values', [])

    def select_data(self, title: str,
                    sql_query: str,
                    response_type: ResponseType = RESPONSE_TYPE) -> Answer:

        data = self.read_all_data_from_sheet(title)

        columns = data[0]
        data.pop(0)

        df = pd.DataFrame(data, columns=columns)

        new_query = sql_query.replace(title, "df", 1)

        result = ps.sqldf(new_query)

        if response_type is ResponseType.Value:
            return Answer(Request={"request": sql_query}, Response=self.__dataframe_to_value(result))

        if response_type is ResponseType.List:
            return Answer(Request={"request": sql_query}, Response=result.values.tolist())

        if response_type is ResponseType.DataFrame:
            return Answer(Request={"request": sql_query}, Response=result)

    def __dataframe_to_value(self, dataframe):
        dataframe_len = len(dataframe.values.tolist())
        if dataframe_len > 1:
            return dataframe.values.tolist()

        if dataframe_len == 1:
            if len(dataframe.values.tolist()[0]) > 1:
                return dataframe.values.tolist()[0]
            else:
                return dataframe.values.tolist()[0][0]

    def insert_data(self, title: str, data: str, columns: List[str]=None) -> Answer:

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.table_id,
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

        response = self.service.spreadsheets().values().append(
            spreadsheetId=self.table_id,
            range=title,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=value_range_body
        ).execute()

        return Answer(Request=value_range_body, Response=response)

    def delete_rows(self, title: str, sql_query: str) -> Answer:
        values_to_delete = self.select_data(title, sql_query, ResponseType.List)
        print(values_to_delete)

        range_name = f'{title}!A2:ZZ'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.table_id,
            range=range_name).execute()

        values = result.get('values', [])

        sheet_properties = self.get_sheet_properties_by_name(title)
        sheet_id = sheet_properties['sheetId']

        if not values:
            return Answer(Request=None, Response={"response": "Table is empty"})

        rows_to_delete = []

        for i, row in enumerate(values):
            print(row)
            if row in values_to_delete:
                rows_to_delete.append(i + 1)

        rows_to_delete.sort(reverse=True)# Это полная жопа


        if not rows_to_delete:
            return Answer(Request=None, Response={"response": "Rows to delete not found"})

        request = [
                {
                    'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': row_index,
                        'endIndex': row_index + 1
                        }
                    }

                }
                for row_index in rows_to_delete

            ]

        response = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.table_id,
                    body={'requests': request}
                ).execute()

        return Answer(Request=request, Response=response)






