from flask import Flask
from flask_restful import Resource, Api

from .message import Message

def get_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Message, '/message')
    return app



