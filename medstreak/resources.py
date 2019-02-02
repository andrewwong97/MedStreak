from flask import Flask
from flask_restful import Resource, Api
from bson.json_util import dumps
from database import getDB


class User(Resource):
    def get(self, user_id=None):
        db = getDB()
        if user_id:
            # return user information
            pass
        else:
            # return all users
            return dumps(db.users.find())

    def post(self, id=None):
        #login with username/password
        pass

    def put(self, id=None):
        #signup with user information
        pass


class Medication(Resource):
    pass
