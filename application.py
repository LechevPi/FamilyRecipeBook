from flask import Flask


def create_app():
    application = Flask(__name__)

    @application.route("/")
    def hello():
        return "Hello Pierre - This is a one step!"

    return application

if __name__ == "__main__":
    application = create_app()

