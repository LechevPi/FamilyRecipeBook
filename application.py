from flask import Flask
from flask_basicauth import BasicAuth


def create_app():
    application = Flask(__name__)

    # Creation of the basic authentification object
    basic_auth = BasicAuth(application)

    @application.route("/")
    def hello():
        return "Hello Pierre - This is a one step!"

    return application

if __name__ == "__main__":
    application = create_app()

