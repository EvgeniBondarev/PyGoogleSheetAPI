from typing import List, Optional, Tuple

from .data_difinition import DataDefinition
from .data_manipulation import DataManipulation
from .sql_parser import SQLParser
from .dataclasses import GsDataBase, Answer, ResponseType
import gs_sql.configuration as  configuration


class SheetsQL:
    def __init__(self):
        self.data_difinition = None
        self.data_manipulation = None
        self.sql_processor = None

    def authorization(self, credentials: str):
        self.data_difinition = DataDefinition(credentials)
        self.data_manipulation = DataManipulation(credentials)

        self.sql_processor = SQLParser(self.data_difinition, self.data_manipulation)

    def connect(self, table_data: GsDataBase):
        self.data_difinition.connect(table_data)
        self.data_manipulation.connect(table_data)

    def set_configuration(self,
                          response_type: ResponseType,
                          colum_color: Optional[List[Tuple[float, float, float]]]):
        configuration.RESPONSE_TYPE = response_type
        configuration.COLUMN_COLOR = colum_color

    def execute(self, sql_query: str) -> Answer:
        return self.sql_processor.execute(sql_query)




