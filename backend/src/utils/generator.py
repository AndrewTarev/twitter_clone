import time
import random
import threading

import requests

endpoints = ("one", "two", "three", "four", "error")


def run():
    while True:
        try:
            "curl - X"
            "POST" "http://0.0.0.0:8000/api/tweets" "- H"
            "accept: application/json" "- H"
            "api-key: e1208129f1abc28a39efca50556fdaa2aaa7fcde" "- H"
            "Content-Type: application/json" "- d"
            '{"tweet_data": "Привет",}'
        except:
            pass


if __name__ == "__main__":
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)
