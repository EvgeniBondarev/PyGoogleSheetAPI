import re
from enum import Enum

from .Exceptions import *
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

    # def connect(self, table_data):
    #     return self.data_manipulation.connect(table_data)

    def execute(self, sql_query: str):

        if sql_query[-1] != ";":
            sql_query += ";"

        sql_type = self.__get_query_type(sql_query)

        #DDL
        if sql_type is QueryType.CREATE:
            return self.__execute_create(sql_query)

        if sql_type is QueryType.ALTER:
            return self.__execute_alert(sql_query)

        if sql_type is QueryType.DROP:
            return self.__execute_drop(sql_query)

        #DML
        if sql_type is QueryType.SELECT:
            a =  self.__execute_select(sql_query)
            return a

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

        table_pattern = r'CREATE TABLE IF NOT EXISTS (\w+)'
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
                    try:
                        result = dd.create_table(table_name, columns)
                    except TableAlreadyExists:
                        result = None

            return result

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




    def __execute_alert(self, sql_query):
        table_pattern = r'ALTER TABLE (\w+)'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)

            # Используем регулярное выражение для извлечения столбцов для изменения
            columns_pattern = r'ALTER COLUMN (.*?);'
            columns_match = re.search(columns_pattern, sql_query)
            if columns_match:
                columns = columns_match.group(1).split(',')

                # Удаляем лишние пробелы и кавычки вокруг имен столбцов
                columns = [column.strip() for column in columns]

                # Выводим название таблицы и столбцы для изменения
                print(f"Table: {table_name}")
                print("Columns to alter:")
                for column in columns:
                    print(column)

                with self.data_difinition as dd:
                    result = dd.update_column(table_name, columns)

                return result

            rename_pattern = r'RENAME COLUMN (\w+) TO (\w+);'
            rename_match = re.search(rename_pattern, sql_query)
            if rename_match:
                old_name = rename_match.group(1)
                new_name = rename_match.group(2)

                # Выводим имя таблицы, старое и новое названия столбца
                print(f"Table: {table_name}")
                print(f"Rename column '{old_name}' to '{new_name}'")

                with self.data_difinition as dd:
                    result = dd.rename_column(table_name, old_name, new_name)

                return result

            delete_pattern = r'ALTER TABLE (\w+)'
            delete_match = re.search(delete_pattern, sql_query)
            if delete_match:
                delete_name = delete_match.group(1)

                # Используем регулярное выражение для извлечения названия удаляемого столбца
                column_pattern = r'DROP COLUMN (\w+);'
                column_match = re.search(column_pattern, sql_query)
                if column_match:
                    column_name = column_match.group(1)

                    # Выводим имя таблицы и название удаляемого столбца
                    print(f"Table: {delete_name}")
                    print(f"Drop column: {column_name}")

                    with self.data_difinition as dd:
                        result = dd.delete_column(table_name, column_name)

                    return result

    def __execute_drop(self, sql_query):
        table_pattern = r'DROP TABLE (\w+);'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)

            print(f"Table to drop: {table_name}")
            with self.data_difinition as dd:
                        result = dd.drop_table(table_name)
        return result

    def __execute_select(self, sql_query):
        table_pattern = r'FROM (\w+)'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)
            result = self.data_manipulation.select_data(table_name, sql_query)

            return result
