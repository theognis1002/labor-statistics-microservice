import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(testing=False):
    app = Flask(__name__)

    from app.views import api

    app.register_blueprint(api)

    return app
