from flask import Flask, current_app, request, jsonify, make_response
from flask_restful import Resource, reqparse
from email.utils import parseaddr

from .database import get_rows_by_range, add_row, get_not_fetched_rows

import json

class Message(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start',
                            type=int,
                            help='Start index',
                            required=False)
        parser.add_argument('end',
                            type=int,
                            help='End index',
                            required=False)
        args = parser.parse_args()

        if args.start is None or args.end is None:
            return get_not_fetched_rows()

        return get_rows_by_range(args.start, args.end)

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

        # validate email
        if '@' not in parseaddr(args.recipient)[1]:
            return make_response(jsonify(message="Incorrect email"), 400)

        # save message
        data = json.dumps({"recipient": args.recipient,
                           "message": args.message}).encode()

        # save: if error, return
        if add_row(data) is False:
            return make_response(jsonify(message="Cannot save messaage"), 500)

        return make_response(jsonify(message="Added"), 201)

