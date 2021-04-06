import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app(testing=False):
    app = Flask(__name__)

    from app.views import api

    # from app.middleware import LoggingMiddleware

    app.register_blueprint(api)
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)

    return app
