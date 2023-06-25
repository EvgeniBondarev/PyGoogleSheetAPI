from gs_api.data_difinition import DataDefinition

from gs_api.file_utils import authorization


authorization("files//credentials.json")

if __name__ == '__main__':

    with DataDefinition() as dd:
        print(dd.user_tables)

        column_names = ['Column 1', 'Column 2', 'Column 3']
        new_sheet_id = dd.create_table('tes2qweaasq', column_names)

        print(dd.user_tables)

        new_column_names = ['NewColumn 1', 'Column 2xcvx', 'Column 3']
        dd.update_table("tes2qweaasq", "nesdf31", new_column_names)

        print(dd.user_tables)


