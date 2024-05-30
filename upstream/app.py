from ddtrace import patch_all, tracer
from flask import Flask
import os
import requests
import time

patch_all()

downstream_host = os.getenv("DOWNSTREAM_HOST") or "localhost"
READ_DELAY = 0
app = Flask(__name__)


@app.route("/new-user/<username>")
def new_user(username):
    r = requests.get("http://" + downstream_host + ":8110/users/" + username)
    return r.json()


@app.route("/list-users")
def list_users():
    with tracer.trace("DELAY"):
        time.sleep(READ_DELAY)
    r = requests.get("http://" + downstream_host + ":8110/users")
    return r.json()


@app.route("/clear-users")
def clear_users():
    r = requests.get("http://" + downstream_host + ":8110/users/delete")
    return r.json()


@app.route("/delay/<seconds>")
def set_delay(seconds):
    global READ_DELAY
    READ_DELAY = float(seconds)
    return "List Users delay set to " + str(READ_DELAY) + " seconds."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100, debug=True)
