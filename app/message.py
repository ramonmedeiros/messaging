from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, reqparse


from .database import add_row
import json

class Message(Resource):

    def get(self):
        # retrieve message
        return {'hello': 'world'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recipient',
                            type=str,
                            location="json",
                            help='Email of the recipient',
                            required=True)
        parser.add_argument('message',
                            type=str,
                            location="json",
                            help='Message content',
                            required=True)
        args = parser.parse_args()

        # save message
        data = json.dumps({"recipient": args.recipient,
                           "message": args.message}).encode()

        # save: if error, return
        if add_row(data) is False:
            return make_response(jsonify(message="Cannot save messaage"), 500)

        return make_response(jsonify(message="Added"), 201)

