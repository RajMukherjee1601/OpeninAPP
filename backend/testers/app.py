import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, path)

import flask
from request.base import Requests

app = flask.Flask(__name__)


@app.route("/text", methods=["POST"])
def main():

    user_request = flask.request.json
    user_request["mode"] = "text"

    # "user_prompt": "My name is An"

    request = Requests(user_request)
    request.handler()


if __name__ == "__main__":
    app.run(debug=True)
