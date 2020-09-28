from flask import g
import sqlite3

DATABASE = "exercise_tracker.db"


def dict_factory(cursor, row):
    """
    Turns rows into dictionaries for easier JSON conversion. Plugs into
    Connection.row_factory.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


def init_db():
    db = get_db()
    c = db.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS User(
            _id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL CHECK (length(username) <= 32)
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Exercise(
            username TEXT,
            userId TEXT NOT NULL,
            description TEXT NOT NULL
                CONSTRAINT description_length CHECK (length(description) <= 32),
            duration INTEGER NOT NULL
                CONSTRAINT duration_minimum CHECK (duration > 0),
            date TEXT NOT NULL
        )
        """
    )
    db.commit()
