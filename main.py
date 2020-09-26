from flask import Flask, g, render_template, request, jsonify, redirect
from exercise import create_new_user, get_all_users, add_exercise, get_exercise_log
import sqlite3
import re

app = Flask("app", static_folder="public", template_folder="views")

DATABASE = "shorturls.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Initialize database
with app.app_context():
    db = get_db()
    c = db.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS User(
            id TEXT PRIMARY KEY,
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
            date REAL DEFAULT (julianday("now"))
        )
        """
    )
    db.commit()


@app.route("/")
def index():
    return render_template("index.html")


app.add_url_rule("/api/exercise/new-user", view_func=create_new_user, methods=["POST"])
app.add_url_rule("/api/exercise/users", view_func=get_all_users, methods=["GET"])
app.add_url_rule("/api/exercise/add", view_func=add_exercise, methods=["POST"])
app.add_url_rule("/api/exercise/log", view_func=get_exercise_log, methods=["GET"])


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
