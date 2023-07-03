import re
from googleapiclient.errors import HttpError
from enum import Enum


class QueryType(Enum):
    CREATE = "CREATE"
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ALTER = "ALTER"
    DROP = "DROP"
    UNKNOWN = "Unknown"

class SQLProcessor():

    def __init__(self, data_difinition, data_manipulation=None):
        self.data_difinition = data_difinition
        self.data_manipulation = data_manipulation

    def execute(self, sql_query):
        if not self.data_difinition.table_id:
            raise ConnectionError()

        if sql_query[-1] != ";":
            sql_query += ";"

        sql_type = self.__get_query_type(sql_query)
        print(sql_type)

        #DDL
        if sql_type is QueryType.CREATE:
            return self.__execute_create(sql_query)

        if sql_type is QueryType.ALTER:
            return self.__execute_alert(sql_query)

        if sql_type is QueryType.DROP:
            return self.__execute_drop(sql_query)

        #DML
        if sql_type is QueryType.SELECT:
            #TODO: Трабл
            a = self.__execute_select(sql_query)
            return a

        if sql_type is QueryType.INSERT:
            return self.__execute_inset(sql_query)

    def __get_query_type(self, sql_query):
        if re.search(r'^\s*CREATE', sql_query, re.IGNORECASE):
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

                try:
                    result = self.data_difinition.create_table(table_name, columns)
                    return result

                except HttpError:
                    return None




        table_pattern = r'CREATE TABLE (\w+)'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)

            column_pattern = r'\((.*?)\)'
            column_match = re.search(column_pattern, sql_query)
            if column_match:
                columns = column_match.group(1).split(',')

                columns = [column.strip().strip('"') for column in columns]

                result = self.data_difinition.create_table(table_name, columns)

            return result

        base_pattern = r'CREATE DATABASE (\w+)'
        table_match = re.search(base_pattern, sql_query)
        if table_match:
            base_name = table_match.group(1)

            result = self.data_difinition.create_database(base_name)

            return result




    def __execute_alert(self, sql_query):
        table_pattern = r'ALTER TABLE (\w+)'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)

            columns_pattern = r'ALTER COLUMN (.*?);'
            columns_match = re.search(columns_pattern, sql_query)
            if columns_match:
                columns = columns_match.group(1).split(',')

                columns = [column.strip() for column in columns]

                for column in columns:
                    print(column)


                result = self.data_difinition.alert_column(table_name, columns)

                return result

            rename_pattern = r'RENAME COLUMN (\w+) TO (\w+);'
            rename_match = re.search(rename_pattern, sql_query)
            if rename_match:
                old_name = rename_match.group(1)
                new_name = rename_match.group(2)


                result = self.data_difinition.rename_column(table_name, old_name, new_name)

                return result

            delete_pattern = r'ALTER TABLE (\w+)'
            delete_match = re.search(delete_pattern, sql_query)
            if delete_match:
                delete_name = delete_match.group(1)

                column_pattern = r'DROP COLUMN (\w+);'
                column_match = re.search(column_pattern, sql_query)
                if column_match:
                    column_name = column_match.group(1)

                    result = self.data_difinition.delete_column(delete_name, column_name)

                    return result

    def __execute_drop(self, sql_query):
        table_pattern = r'DROP TABLE (\w+);'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)

            result = self.data_difinition.drop_table(table_name)

        return result

    def __execute_select(self, sql_query):
        table_pattern = r'FROM (\w+)'
        table_match = re.search(table_pattern, sql_query)
        if table_match:
            table_name = table_match.group(1)
            result = self.data_manipulation.select_data(table_name, sql_query)
            return result

    def __execute_inset(self, sql_query):
        table_pattern = r'INSERT INTO (\w+)'
        table_match = re.search(table_pattern, sql_query)
        columns = values = table_name = None
        if table_match:
            table_name = table_match.group(1)

            values_pattern = r'VALUES \((.*?)\)'
            values_match = re.search(values_pattern, sql_query)
            if values_match:
                values = values_match.group(1).split(',')

                values = [value.strip() for value in values]

            column_pattern = rf'{table_name} \((.*?)\)'
            column_match = re.search(column_pattern, sql_query)
            if column_match:
                columns = column_match.group(1).split(',')

                columns = [column.strip() for column in columns]

            result = self.data_manipulation.insert_data(table_name, values, columns)

            return result