from gs_api.sheetsql import SheetsQL
from gs_api.data_difinition import DataDefinition
from pprint import pprint
from gs_api.dataclasses import GsDataBase

# SQL COMMANDS: http://www.postgresql.org/docs/8.3/interactive/sql-commands.html
if __name__ == '__main__':
    sql = SheetsQL()

    sql.authorization("files//credentials.json")

    # res = sql.execute("CREATE DATABASE TestBase")
    #391_zzvvCQyOiwHiBGM7tICiDUUm8iTIGEQBs1tVRYo1

    sql.connect(GsDataBase("1391_zzvvCQyOiwHiBGM7tICiDUUm8iTIGEQBs1tVRYo", "TestBase"))
    # create = sql.execute("CREATE TABLE 1 (id, first_name, last_name, email, gender, ip_address)")
    # move = sql.execute("ALTER TABLE 1 ALTER COLUMN ID, first_name, last_name, email, gender, ip_address")
    # rename = sql.execute("ALTER TABLE 1 RENAME COLUMN email TO Email")
    # delete = sql.execute("DROP TABLE 1")
    select = sql.execute("SELECT * FROM Users WHERE id = '10'")
    print(select)








