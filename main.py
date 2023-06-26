from gs_api.sheetsql import SheetsQL



if __name__ == '__main__':
    sql = SheetsQL()

    sql.authorization("files//credentials.json")

    move = sql.execute("CREATE TABLE users(id, name)")

    print(move)





