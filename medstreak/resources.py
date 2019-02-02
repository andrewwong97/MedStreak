from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient(
    'mongodb://medstreak:medstreak@medstreak-dev-shard-00-00-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-01-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-02-8ghe7.mongodb.net:27017/medstreak-dev?ssl=true&replicaSet=MedStreak-Dev-shard-0&authSource=admin&retryWrites=true')
db = client['medstreak-dev']


class User(Resource):
    def get(self, user_id=None):
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
