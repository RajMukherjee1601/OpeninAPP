import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)


from request.base import Requests


def main():

    user_request = [
        {"user_prompt": "President will be taking his oath on 2nd October", "mode": "text"},
        {"user_prompt": "input", "mode": "pdf"},
        {"user_prompt": "Break a leg", "mode": "text"},
    ]
    request = Requests(user_request[-1])
    request.handler()


if __name__ == "__main__":
    main()
