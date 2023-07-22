from gs_api.sheetsql import SheetsQL
from gs_api.dataclasses import GsDataBase

# SQL COMMANDS: http://www.postgresql.org/docs/8.3/interactive/sql-commands.html
if __name__ == '__main__':
    sql = SheetsQL()

    sql.authorization("files//credentials.json")

    sql.connect(GsDataBase(id="1k34kd8Cw4IT6jK7O0q06r-egBY1mSXu7su0ZLemR8Zk", name="Users"))

    query = sql.execute("""SELECT UserData.name, UserData.password, Chats.message
                            FROM UserData
                            INNER JOIN Chats ON UserData.id=Chats.user;""")


    print(query.Response)













