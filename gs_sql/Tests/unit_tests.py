from unittest import TestCase, main

from gs_sql.sheetsql import SheetsQL
from gs_sql.dataclasses import GsDataBase, ResponseType



class SheetsQLTests(TestCase):
    def setUp(self):
        self.sheetsql = SheetsQL()

    def test_authorization(self):
        credentials = r"C:\users\Evgeni\Desktop\api\files\credentials.json"
        self.sheetsql.authorization(credentials)
        self.assertIsNotNone(self.sheetsql.data_difinition)
        self.assertIsNotNone(self.sheetsql.data_manipulation)
        self.assertIsNotNone(self.sheetsql.sql_processor)

    # def test_connect(self):
    #     table_data = GsDataBase()
    #     self.sheetsql.connect(table_data)
    #     # Add assertions to check if connection is established correctly
    #
    # def test_set_configuration(self):
    #     response_type = ResponseType.JSON
    #     column_color = [(0.5, 0.5, 0.5), (0.3, 0.3, 0.3)]
    #     self.sheetsql.set_configuration(response_type, column_color)
    #     self.assertEqual(self.sheetsql.RESPONSE_TYPE, response_type)
    #     self.assertEqual(self.sheetsql.COLUMN_COLOR, column_color)



if __name__ == '__main__':
    main()