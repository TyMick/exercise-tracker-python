from flask import request, jsonify, redirect
from database import get_db
import nanoid


def dict_factory(cursor, row):
    """
    Turns rows into dictionaries for easier JSON conversion. Plugs into
    Connection.row_factory.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_new_user(): # test _id: J9LyZZ9VPD
    username = request.form["username"]
    _id = nanoid.generate(
        alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        size=10,
    )

    try:
        db = get_db()
        db.cursor().execute(
            "INSERT INTO User(_id, username) VALUES(?, ?)", (_id, username)
        )
        db.commit()
        return jsonify(username=username, _id=_id)
    except:
        return jsonify(error="database error")


def get_all_users():
    try:
        db = get_db()
        db.row_factory = dict_factory
        c = db.cursor()
        c.execute("SELECT username, _id FROM User")
        return jsonify(c.fetchall())
    except:
        return jsonify(error="database error")


def add_exercise():
    pass


def get_exercise_log():
    pass
