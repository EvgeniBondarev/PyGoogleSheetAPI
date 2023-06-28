class SheetsQLException(Exception):
     """Basic class"""

class TableAlreadyExists(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"Table named '{table_name}' already exists!" )

class TableNotFound(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"Table named {table_name} not found!" )

class TableWrongSize(SheetsQLException):
    def __init__(self, table_name):
        super().__init__(f"The number of new column names exceeds the number of columns in the table. Table: '{table_name}'")

# class TableNameUniqueness(Exception):
#     pass