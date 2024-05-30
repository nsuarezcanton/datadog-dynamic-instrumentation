from ddtrace import patch_all, tracer
from ddtrace.debugging import DynamicInstrumentation
from flask import Flask
import os
import redis
import time
import uuid

DynamicInstrumentation.enable()
patch_all()

r = redis.Redis(
    host=os.getenv("REDIS_HOST") or "localhost",
    port=6379,
    db=0,
    decode_responses=True,
)
READ_DELAY = 0
app = Flask(__name__)


@app.route("/users/<username>")
def create_user(username):
    id = str(uuid.uuid4())
    r.set(id, username)
    return [username, id]


@app.route("/users")
def read_users():
    with tracer.trace("DELAY"):
        time.sleep(READ_DELAY)
    users = []
    for key in r.scan_iter("*"):
        users.append(key)
    return users


@app.route("/users/delete")
def delete_users():
    for key in r.scan_iter("*"):
        r.delete(key)
    return []


@app.route("/delay/<seconds>")
def set_delay(seconds):
    global READ_DELAY
    READ_DELAY = float(seconds)
    return "Read Users delay set to " + str(READ_DELAY) + " seconds."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8110, debug=True)
