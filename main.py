from gs_api.sheetsql import SheetsQL
from pprint import pprint


if __name__ == '__main__':
    sql = SheetsQL()

    sql.authorization("files//credentials.json")

    # move = sql.execute("CREATE TABLE Users (id, first_name, last_name, email, gender, ip_address)")
    # print(move)

    #move = sql.execute("ALTER TABLE Test RENAME COLUMN name TO Nee")

    # move = sql.execute("ALTER TABLE Test DROP COLUMN id")
    #
    #move = sql.execute("SELECT  FROM Test WHERE name = 'Газ'")
    move = sql.execute("INSERT INTO Users (id, first_name, last_name, emailqwe, gender, ip_address) VALUES (1001, evgen, bondarev, tetst, m, 123232.324324);")
    print(move)





