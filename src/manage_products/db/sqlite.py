import sqlite3

SQLITE_DATABASE_URI = "./manage_products/products.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_connect():
    conn = sqlite3.connect(SQLITE_DATABASE_URI)
    conn.row_factory = dict_factory
    return conn


def read(query, params=None, one=False):
    try:
        conn = db_connect()
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        if one:
            return cur.fetchone()
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"[SQLITE READ ERROR] {e.args[0]}")
        return False


def write(query, params=None, lastrowid=False):
    try:
        conn = db_connect()
        cur = conn.cursor()
        if cur.execute(query, params):
            conn.commit()
            if lastrowid:
                return cur.lastrowid
            return True
        return False
    except sqlite3.Error as e:
        print(f"[SQLITE WRITE ERROR] {e.args[0]}")
        return False
