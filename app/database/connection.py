import sqlite3


def get_connection():
    with sqlite3.connect("app/database/parser.db") as conn:
        yield conn
