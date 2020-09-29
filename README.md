# Python exercise tracker

[![Run on Repl.it](https://repl.it/badge/github/tywmick/exercise-tracker-python)](https://repl.it/github/tywmick/exercise-tracker-python)

This is a Python port of my [Node.js exercise tracker](https://ty-exercise-tracker.glitch.me/), built with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLite](https://sqlite.org/index.html). The front end API on the home page also uses [Bootstrap](https://getbootstrap.com/), [jQuery](https://jquery.com/), [jQuery UI](https://github.com/dylang/shortid), and [highlight.js](https://highlightjs.org/). The API fulfills the following user stories:

1. I can create a user by posting form data username to `/api/exercise/new-user` and returned will be an object with `username` and `_id`.
2. I can get an array of all users by getting `api/exercise/users` with the same info as when creating a user.
3. I can add an exercise to any user by posting form data `userId` (`_id`), `description`, `duration`, and optionally `date` to `/api/exercise/add`. If no date supplied it will use current date. Returned will the the user object with also with the exercise fields added.
4. I can retrieve a full exercise log of any user by getting `/api/exercise/log` with a parameter of `userId` (`_id`). Return will be the user object with added array log and count (total exercise count).
5. I can retrieve part of the log of any user by also passing along optional parameters of `from` & `to` or `limit`. (Date format `yyyy-mm-dd`, `limit` = int)
