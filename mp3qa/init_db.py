import os
import sqlite3


def init_db(database: str = ':memory:'):
    con = sqlite3.connect(database)
    with open(os.path.join(os.path.dirname(__file__), 'init_db.sql'), 'rt') as sqlfile:
        con.cursor().executescript(sqlfile.read())
        con.commit()

    return con
