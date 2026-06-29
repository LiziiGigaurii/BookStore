import sqlite3

from flask_login import LoginManager

login_manager = LoginManager()

DATABASE_PATH = "database.db"


def get_db():
    """Open a new database connection with row access by column name."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def set_database_path(path):
    """Allow app.py to point this module at a configured DB file path."""
    global DATABASE_PATH
    DATABASE_PATH = path