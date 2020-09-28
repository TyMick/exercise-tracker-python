from flask import Flask, g, render_template
from database import init_db
from api.exercise import create_new_user, get_all_users, add_exercise, get_exercise_log

app = Flask("app", static_folder="public", template_folder="views")

with app.app_context():
    init_db()


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
