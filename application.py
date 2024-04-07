"""Simple Hello World Flask demo app."""

from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello Pierre - This is a one step!"
