from .Exceptions import *

from .dataclasses import GsDataBase
from .BaseData import BaseData

from typing import List, Optional, Tuple
class DataDefinition(BaseData):
    def create_database(self, spreadsheet_name: str) -> GsDataBase:
        request_body = {
            'properties': {
                'title': spreadsheet_name
            }
        }
        response = self.service.spreadsheets().create(body=request_body).execute()

        return GsDataBase(id=response['spreadsheetId'], name=response['properties']['title'])
    def create_table(self,  sheet_name: str,
                            column_names: List[str],
                            column_colors: Optional[List[Tuple[float, float, float]]] = None) -> dict:

        if column_colors is None:
            column_colors = [(0.85, 0.85, 0.85)] * len(column_names)

        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]

        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={'requests': requests}
        ).execute()


        new_sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']

        update_requests = []
        update_requests.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': new_sheet_id,
                    'gridProperties': {
                        'columnCount': len(column_names),
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties(columnCount,frozenRowCount)'
            }
        })

        for i, column_name in enumerate(column_names):
            update_requests.append({
                'updateCells': {
                    'rows': [{
                        'values': [{
                            'userEnteredValue': {
                                'stringValue': column_name
                            },
                            'userEnteredFormat': {
                                'textFormat': {
                                    'bold': True
                                }
                            }
                        }]
                    }],
                    'fields': 'userEnteredValue,userEnteredFormat.textFormat.bold',
                    'start': {
                        'sheetId': new_sheet_id,
                        'rowIndex': 0,
                        'columnIndex': i
                    }
                }
            })

        for i, column_color in enumerate(column_colors):
            update_requests.append({
                'updateCells': {
                    'rows': [{
                        'values': [{
                            'userEnteredFormat': {
                                'backgroundColor': {
                                    'red': column_color[0],
                                    'green': column_color[1],
                                    'blue': column_color[2],
                                    'alpha': 1
                                }
                            }
                        }]
                    }],
                    'fields': 'userEnteredFormat.backgroundColor',
                    'start': {
                        'sheetId': new_sheet_id,
                        'rowIndex': 0,
                        'columnIndex': i
                    }
                }
            })

        self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.table_id,
                body={'requests': update_requests}
        ).execute()

        return response
    def alert_column(self, sheet_title: str,  new_column_names: list[str] = None) -> dict:

        if new_column_names is None:
            new_column_names = self.service.spreadsheets().values().get(spreadsheetId=self.table_id, range='A1:1').execute().get('values')[0]

        sheet_properties = self.get_sheet_properties_by_name(sheet_title)

        column_count = sheet_properties['gridProperties']['columnCount']

        if len(new_column_names) > column_count:
            raise TableWrongSize(sheet_title)

        request_body = {
            'requests': [
                {
                    'updateCells': {
                        'start': {
                            'sheetId': sheet_properties['sheetId'],
                            'rowIndex': 0,
                            'columnIndex': 0
                        },
                        'rows': [
                            {
                                'values': [
                                    {
                                        'userEnteredValue': {
                                            'stringValue': name
                                        }
                                    } for name in new_column_names
                                ]
                            }
                        ],
                        'fields': 'userEnteredValue'
                    }
                }
            ]
        }

        result = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body=request_body
        ).execute()

        return result

    def rename_column(self, sheet_title: str, old_column_name: str, new_column_name: str) -> dict:

        sheet_properties = self.get_sheet_properties_by_name(sheet_title)
        sheet_id = sheet_properties['sheetId']
        old_column_index = self.get_column_index_by_name(sheet_title, old_column_name)


        requests = [
            {
                'updateCells': {
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredValue': {
                                        'stringValue': new_column_name
                                    }
                                }
                            ]
                        }
                    ],
                    'fields': 'userEnteredValue',
                    'start': {
                        'sheetId': sheet_id,
                        'rowIndex': 0,
                        'columnIndex': old_column_index
                    }
                }
            }
        ]

        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={'requests': requests}
        ).execute()

        return response


    def delete_column(self, sheet_title: str, column_name: str) -> dict:
        sheet_properties = self.get_sheet_properties_by_name(sheet_title)

        sheet_id = sheet_properties['sheetId']
        column_index = self.get_column_index_by_name(sheet_title, column_name)

        requests = [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': column_index,
                        'endIndex': column_index + 1
                    }
                }
            }
        ]

        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={'requests': requests}
        ).execute()

        return response

    def drop_table(self, sheet_title: str) -> dict:

        sheet_properties = self.get_sheet_properties_by_name(sheet_title)

        sheet_id = sheet_properties['sheetId']

        requests = [
            {
                'deleteSheet': {
                    'sheetId': sheet_id
                }
            }
        ]

        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={'requests': requests}
        ).execute()

        return response