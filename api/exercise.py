from flask import request, jsonify, redirect
from database import get_db
import nanoid


def create_new_user(): # test userid: KGqwTYf4HH
    username = request.form["username"]
    user_id = nanoid.generate(
        alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        size=10,
    )

    db = get_db()
    db.cursor().execute(
        "INSERT INTO User(id, username) VALUES(?, ?)", (user_id, username)
    )
    db.commit()
    return jsonify(username=username, _id=user_id)


def get_all_users():
    pass


def add_exercise():
    pass


def get_exercise_log():
    pass
