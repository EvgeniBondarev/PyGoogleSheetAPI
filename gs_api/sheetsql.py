import re
from enum import Enum
from functools import singledispatch

from .data_difinition import DataDefinition
from .data_manipulation import DataManipulation
from .file_utils import authorization


class QueryType(Enum):
    CREATE = "CREATE"
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ALTER = "ALTER"
    DROP = "DROP"
    UNKNOWN = "Unknown"



class SheetsQL:

    def __init__(self):
        self.data_difinition = None
        self.data_manipulation = None

    def authorization(self, credentials: str):
        authorization(credentials)

        self.data_difinition = DataDefinition()
        self.data_manipulation = DataManipulation()

    def execute(self, sql_query: str):
        sql_type = self.__get_query_type(sql_query)

        if sql_type is QueryType.CREATE:
            self.__execute_create(sql_query)

        if sql_type is QueryType.SELECT:
            self.__execute_select(sql_query)


    def __get_query_type(self, sql_query):
        if re.search(r'^\s*CREATE\s+TABLE', sql_query, re.IGNORECASE):
            query_type = QueryType.CREATE

        elif re.search(r'^\s*SELECT', sql_query, re.IGNORECASE):
            query_type = QueryType.SELECT

        elif re.search(r'^\s*INSERT', sql_query, re.IGNORECASE):
            query_type = QueryType.INSERT

        elif re.search(r'^\s*UPDATE', sql_query, re.IGNORECASE):
            query_type = QueryType.UPDATE

        elif re.search(r'^\s*ALTER', sql_query, re.IGNORECASE):
            query_type = QueryType.ALTER

        elif re.search(r'^\s*DELETE', sql_query, re.IGNORECASE):
            query_type = QueryType.DELETE

        elif re.search(r'^\s*DROP', sql_query, re.IGNORECASE):
            query_type = QueryType.DROP

        else:
            query_type = QueryType.UNKNOWN

        return query_type

    def __execute_create(self, sql_query):

        table_pattern = r'CREATE TABLE (\w+)'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)

            column_pattern = r'\((.*?)\)'
            column_match = re.search(column_pattern, sql_query)
            if column_match:
                columns = column_match.group(1).split(',')

                columns = [column.strip().strip('"') for column in columns]

                print(f"Table: {table_name}")
                print(f"Columns: {columns}")

                with self.data_difinition as dd:
                    result = dd.create_table(table_name, columns)
                    return result



    def __execute_select(self, sql_query):
        print("select")
