from flask import g
import sqlite3

DATABASE = "exercise_tracker.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
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
            description TEXT NOT NULL,
            duration INTEGER NOT NULL CHECK (duration > 0),
            date REAL NOT NULL
        )
        """
    )
    db.commit()
