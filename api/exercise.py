from flask import request, jsonify, redirect
from database import get_db
from datetime import date as py_date
import sqlite3
import nanoid


def create_new_user():
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
        return {"username": username, "_id": _id}
    except sqlite3.IntegrityError as e:
        if e.args[0] == "UNIQUE constraint failed: User.username":
            return {"error": "Username already exists"}
        elif e.args[0] == "CHECK constraint failed: User":
            return {"error": "Username cannot be longer than 32 characters"}
    except:
        return {"error": "Database error"}


def get_all_users():
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT username, _id FROM User")
        users = c.fetchall()
        return jsonify(users)
    except:
        return {"error": "Database error"}


def add_exercise():
    # Validate date input
    if request.form["date"]:
        try:
            date = py_date.fromisoformat(request.form["date"])
        except ValueError:
            return {"error": "Invalid date input"}
    else:
        date = py_date.today()

    try:
        db = get_db()
        c = db.cursor()

        # Check for userId
        user_id = request.form["userId"]
        c.execute("SELECT username, _id FROM User WHERE _id = ?", (user_id,))
        user = c.fetchone()
        if user is None:
            return {"error": "No such userId"}

        username = user["username"]
        description = request.form["description"]
        duration = int(request.form["duration"])
        c.execute(
            """
            INSERT INTO Exercise(username, userId, description, duration, date)
            VALUES(?, ?, ?, ?, ?)
            """,
            (username, user_id, description, duration, date.isoformat()),
        )
        db.commit()

        return {
            "username": username,
            "userId": user_id,
            "description": description,
            "duration": duration,
            "date": date.isoformat(),
        }

    except sqlite3.IntegrityError as e:
        if "description_length" in e.args[0]:
            return {"error": "Description cannot be longer than 32 characters"}
        elif "duration_minimum" in e.args[0]:
            return {"error": "Duration must be positive"}
    except:
        return {"error": "Database error"}


def get_exercise_log():
    pass
