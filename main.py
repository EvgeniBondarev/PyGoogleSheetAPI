from gs_api.sheetsql import SheetsQL
from pprint import pprint


if __name__ == '__main__':
    sql = SheetsQL()

    sql.authorization("files//credentials.json")

    move = sql.execute("CREATE TABLE Test (id, name, gender, age)")
    pprint(move)

    #move = sql.execute("ALTER TABLE Test RENAME COLUMN name TO Nee")

    # move = sql.execute("ALTER TABLE Test DROP COLUMN id")
    #
    # move = sql.execute("SELECT * FROM Test WHERE id = 'Запах'")
    # pprint(move)





