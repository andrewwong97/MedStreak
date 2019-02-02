from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient(
    'mongodb://medstreak:medstreak@medstreak-dev-shard-00-00-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-01-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-02-8ghe7.mongodb.net:27017/medstreak-dev?ssl=true&replicaSet=MedStreak-Dev-shard-0&authSource=admin&retryWrites=true')
db = client['medstreak-dev']


class users(Resource):
    def get(self, user_id=None):
        if user_id:
            return dumps(db.users.find({ '_id.$oid': user_id }))
        users = db.users.find()
        return dumps(users)