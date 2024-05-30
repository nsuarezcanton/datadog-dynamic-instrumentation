from ddtrace import patch_all
import requests
import time
import os

patch_all()

upstream_host = os.getenv("UPSTREAM_HOST") or "localhost"

while 1:
    user_count = 0
    start_time = time.time()
    print("START")
    print(time.strftime("%H:%M:%S", time.localtime(start_time)))
    while user_count < 500:
        user_count = user_count + 1
        r = requests.get("http://" + upstream_host + ":8100/new-user/jerry-garcia")
        if user_count % 2 == 0:
            r = requests.get("http://" + upstream_host + ":8100/list-users")
        time.sleep(0.12)
    end_time = time.time()
    print("END")
    print(time.strftime("%H:%M:%S", time.localtime(end_time)))
    r = requests.get("http://" + upstream_host + ":8100/clear-users")
