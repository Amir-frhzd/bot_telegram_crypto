import sqlite3

DATABASE_NAME = "bot_users.db"
def get_connection():

    return sqlite3.connect(DATABASE_NAME)
