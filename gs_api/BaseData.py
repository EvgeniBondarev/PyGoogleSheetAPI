from .authorization import authenticate
from .dataclasses import GsDataBase
from .Exceptions import *

class BaseData:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = None
        self.__authenticate(credentials)

        self.table_id = None
        self.table_name = None


    def __authenticate(self, credentials):
        self.service = authenticate(credentials)

    def connect(self, table_data: GsDataBase):
        self.table_id = table_data.id
        self.table_name = table_data.name

    def get_sheet_properties_by_name(self, sheet_title):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.table_id).execute()
        sheet_properties = None

        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == sheet_title:
                sheet_properties = sheet['properties']
                break

        if sheet_properties is None:
            raise TableNotFound(sheet_title)

        return sheet_properties

    def get_column_index_by_name(self, sheet_title, user_column_name):
        sheet_properties = self.get_sheet_properties_by_name(sheet_title)

        column_count = sheet_properties['gridProperties']['columnCount']

        search_index = None
        for i in range(column_count):
            column_name = self.service.spreadsheets().values().get(spreadsheetId=self.table_id,
                                                                   range=f"{sheet_title}!{chr(65 + i)}1").execute().get('values')[0][0]
            if column_name == user_column_name:
                search_index = i
                break

        if search_index is None:
            raise InvalidColumnName(sheet_title, user_column_name)

        return search_index