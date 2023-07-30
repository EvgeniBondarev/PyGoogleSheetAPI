class SheetsQLException(Exception):
     """Basic class"""

class ConnectionError(SheetsQLException):
    def __init__(self):
        super().__init__(f"Not connected to GoogleShet table! 'SheetsQL().connect(GsDataBase(id, name))'")
class TableAlreadyExists(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"Table named '{table_name}' already exists!" )

class TableNotFound(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"Table named {table_name} not found!" )

class TableWrongSize(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"The number of new column names exceeds the number of columns in the table. Table: '{table_name}'")

class TableEmpty(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"The table is empty and has no column titles. Table: '{table_name}'")

class NumberOfColumns(SheetsQLException):
        def __init__(self, columns, values):
            super().__init__(f"The number of columns ({len(columns)}) does not match the number of data ({len(values)})'")

class InvalidColumnName(SheetsQLException):
    def __init__(self, table, column):
            super().__init__(f"Column '{column}' not found in table '{table}'")

# class TableNameUniqueness(Exception):
#     pass