from flask import Flask
from flask_restful import Resource, Api

from .message import Message
from .database import get_conn

import logging

def get_app():
    # start logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger()

    # start app and api
    app = Flask(__name__)
    api = Api(app)

    # connect db
    app.config.db = get_conn()

    # add handler
    api.add_resource(Message, '/message')
    return app



