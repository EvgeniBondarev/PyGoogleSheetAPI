from dataclasses import dataclass
from enum import Enum


@dataclass
class GsDataBase:
    id: str
    name: str

@dataclass
class Answer:
    Request: list or dict
    Response: list or dict or str

#TODO: Добавить тип sql query