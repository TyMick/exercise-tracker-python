from flask import request, jsonify, redirect
from database import get_db
import nanoid


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
        return jsonify(error="database error", code=500)


def get_all_users():
    pass


def add_exercise():
    pass


def get_exercise_log():
    pass
