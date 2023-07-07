
from .data_difinition import DataDefinition
from .data_manipulation import DataManipulation
from .sql_processor import SQLProcessor
from .dataclasses import GsDataBase, Answer



class SheetsQL():

    def __init__(self):
        self.data_difinition = None
        self.data_manipulation = None
        self.sql_processor = None

    def authorization(self, credentials: str):
        self.data_difinition = DataDefinition(credentials)
        self.data_manipulation = DataManipulation(credentials)

        self.sql_processor = SQLProcessor(self.data_difinition, self.data_manipulation)

    def connect(self, table_data: GsDataBase):
        self.data_difinition.connect(table_data)
        self.data_manipulation.connect(table_data)

    def execute(self, sql_query: str) -> Answer:
        return self.sql_processor.execute(sql_query)




