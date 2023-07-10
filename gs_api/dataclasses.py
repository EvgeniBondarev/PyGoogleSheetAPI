from dataclasses import dataclass
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
class ResponseType(Enum):
    DataFrame = "DataFrame"
    List = "List"
    Value = "Value"

@dataclass
class GsDataBase:
    id: str
    name: str

@dataclass
class Answer:
    Request: list or dict
    Response: list or dict or str

#TODO: Добавить тип sql query