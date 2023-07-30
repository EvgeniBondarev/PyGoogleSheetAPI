# gs-sql

![PyPI](https://img.shields.io/pypi/v/gs-sql?color=orange) ![Python 3.6, 3.7, 3.8](https://img.shields.io/pypi/pyversions/clubhouse?color=blueviolet) ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/EvgeniBondarev/PyGoogleSheetAPI?color=blueviolet) ![License](https://img.shields.io/pypi/l/gs-sql?color=blueviolet) ![Forks](https://img.shields.io/github/forks/EvgeniBondarev/PyGoogleSheetAPI?style=social)

**gs-sql** - 
this module is a Python client library for the GoogleSheetAPI data project management platform using SQL

## Installation

Install the current version with PyPI:

```python
pip install gs-sql
```

Or from Github:
```python
https://github.com/EvgeniBondarev/PyGoogleSheetAPI/archive/refs/heads/main.zip
```

## Usage

At the first login, a browser window will open for confirmation, and a token.pickle file will be created in the directory where your credentials.json file is located to interact with the API.

```python
from gs_api.sheetsql import SheetsQL

gs = SheetsQL()

gs.authorization("files//credentials.json")
```
Afterwards, you can create a table/database in Google Sheets either using standard methods or through SQL queries.
```python
from gs_api.dataclasses import GsDataBase

new_base = gs.execute("""CREATE DATABASE NewBase""")

gs.connect(new_base) # or gs.connect(GsDataBase(id="1fB_1uqU8FklXAQdn9XG4QK3HG4l5U0_vvM3abQ3aiuE", name="NewBase"))
```
Finally, you can now create your first table.
```python
query = gs.execute("CREATE TABLE Users (id, name)")
```
Final code.
```python
from gs_api.sheetsql import SheetsQL


gs = SheetsQL()

gs.authorization("files//credentials.json")

new_base = gs.execute("""CREATE DATABASE NewBase""")

gs.connect(new_base)

query = gs.execute("CREATE TABLE Users (id, name)")
print(query)
```
## Available types of sql queries
### DDL

| No. | Command | Description                                                                        |
|----|--------|------------------------------------------------------------------------------------|
| 1  | CREATE | Creates a new table, view, or other object in the database                         |
| 2  | ALTER  | Modifies an existing object in the database, such as a table                        |
| 3  | DROP   | Deletes an existing table, view, or other object in the database                   |

### DML

| N  | Command | Description                                       |
|----|---------|---------------------------------------------------|
| 1  | SELECT  | Extracts records from one or more tables         |
| 2  | INSERT  | Creates records                                   |
| 3  | UPDATE  | Modifies records                                  |
| 4  | DELETE  | Deletes records                                   |

## Examples
#### CREATE DATABASE
```python
gs = SheetsQL()

gs.authorization("files//credentials.json")

new_base = gs.execute("""CREATE DATABASE NewBase""")

sql.connect(new_base)
```
#### CREATE TABLE
```python
 query = gs.execute("CREATE TABLE Users (id, name)")
```
```python
 query = gs.execute("CREATE TABLE IF NOT EXISTS Users (id, name)")
```
#### ALTER TABLE
```python
query = gs.execute("ALTER TABLE Users DROP COLUMN id;")
```
```python
query = gs.execute("ALTER TABLE Users RENAME COLUMN name TO userName;")
```
```python
query = gs.execute("ALTER TABLE Users ALTER COLUMN NewId, NewName;")
```
#### DROP TABLE
```python
query = gs.execute("DROP TABLE Users;")
```
#### SELECT
```python
query = gs.execute("SELECT * FROM tableName;")
```
```python
query = gs.execute("SELECT col1, col2, ...colN FROM tableName;")
```
```python
query = gs.execute("SELECT DISTINCT col1, col2, ...colN FROM tableName;")
```
```python
query = gs.execute("""SELECT col1, col2, ...colN
                      FROM tableName
                      WHERE condition;""")
```
```python
query = gs.execute("""SELECT col1, col2, ...colN
                      FROM tableName
                      WHERE condition1 AND|OR condition2;""")
```
```python
query = gs.execute("""SELECT col2, col2, ...colN
                    FROM tableName
                    WHERE colName IN (val1, val2, ...valN);""")
```
```python
query = gs.execute("""SELECT col1, col2, ...colN
                    FROM tableName
                    WHERE colName BETWEEN val1 AND val2;""")
```
```python
query = gs.execute("""SELECT col1, col2, ...colN
                    FROM tableName
                    WHERE colName LIKE pattern;""")
```
```python
query = gs.execute("""SELECT col1, col2, ...colN
                    FROM tableName
                    WHERE condition
                    ORDER BY colName;""")
```
```python
query = gs.execute("""SELECT SUM(colName)
                    FROM tableName
                    WHERE condition
                    GROUP BY colName;""")
```
```python
query = gs.execute("""SELECT COUNT(colName)
                    FROM tableName
                    WHERE condition;""")
```
#### INNER JOIN
```python
query = gs.execute("""SELECT Orders.order_id, Orders.order_date, Customers.     customer_name
                    FROM Orders
                    INNER JOIN Customers ON Orders.customer_id = customer_id""")
```
#### INSERT INTO
```python
query = gs.execute("""INSERT INTO table_name
                    VALUES (value1, value2, value3, ...);""")
```
#### UPDATE
```python
query = gs.execute("""UPDATE table_name
                    SET column1 = value1, column2 = value2, ...
                    WHERE condition;""")
```
#### DELETE 
```python
query = gs.execute("""DELETE FROM table_name WHERE condition;""")
```
---
## Configuration
```python
from gs_api.sheetsql import SheetsQL
from gs_api.dataclasses import ResponseType


gs = SheetsQL()

gs.authorization("files//credentials.json")

sql.set_configuration(colum_color=[(0.85, 0.85, 0.85)], # Color in RGB format
                      response_type=ResponseType.List) # Standard List or Pandas DataFrame
```s