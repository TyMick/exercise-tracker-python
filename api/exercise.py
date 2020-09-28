from flask import request, jsonify, redirect
from database import get_db
from datetime import date as py_date
from collections import OrderedDict
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
    if not request.args["userId"]:
        return {"error": "userId is required"}
    user_id = request.args["userId"]

    from_date = to_date = query_limit = None
    try:
        if request.args["from"]:
            from_date = py_date.fromisoformat(request.args["from"])
        if request.args["to"]:
            to_date = py_date.fromisoformat(request.args["to"])
        if request.args["limit"]:
            query_limit = int(request.args["limit"])
    except ValueError as e:
        if "Invalid isoformat" in e.args[0]:
            return {"error": "Invalid date input"}
        if "invalid literal for int" in e.args[0]:
            return {"error": "Invalid limit input"}

    try:
        db = get_db()
        c = db.cursor()

        c.execute("SELECT username, _id FROM User WHERE _id = ?", (user_id,))
        user = c.fetchone()
        if user is None:
            return {"error": "No such userId"}
        username = user["username"]

        # Build query
        query = "SELECT description, duration, date FROM Exercise WHERE userId == ?"
        params = [user_id]
        if from_date:
            query += " AND date(date) >= date(?)"
            params.append(from_date.isoformat())
        if to_date:
            query += " AND date(date) <= date(?)"
            params.append(to_date.isoformat())
        query += " ORDER BY date(date) DESC"
        if query_limit:
            query += " LIMIT ?"
            params.append(query_limit)

        c.execute(query, tuple(params))

        exercises = c.fetchall()
        return {
            "username": username,
            "_id": user_id,
            "from": from_date.isoformat(),
            "to": to_date.isoformat(),
            "count": len(exercises),
            "log": exercises,
        }

    except:
        return {"error": "Database error"}
