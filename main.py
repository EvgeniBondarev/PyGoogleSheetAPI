from gs_sql.sheetsql import SheetsQL
from gs_sql.dataclasses import ResponseType
from gs_sql.dataclasses import GsDataBase

# SQL COMMANDS: http://www.postgresql.org/docs/8.3/interactive/sql-commands.html
if __name__ == '__main__':
    sql = SheetsQL()

    sql.authorization("files//credentials.json")

    sql.set_configuration(colum_color=[(0.85, 0.85, 0.85)], response_type=ResponseType.List)

    new_base = sql.execute("""CREATE DATABASE NewBase1""")

    sql.connect(new_base)

    query = sql.execute("CREATE TABLE Users (id, name)")
    print(query)














