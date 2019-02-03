from flask import Flask
from flask_restful import Resource, Api
from bson.json_util import dumps
from database import getDB
import hashlib
import bcrypt

class Login(Resource):
    def post(self, id=None):
        #login with email/password, return id
        data = request.get_json()
        email = data['email']
        password = data['password']
        salt = db.users.find_one({'email': email}, {'salt': 1})
        #check user exists
        if not salt:
            return { 'reason': 'Email not registered' }, 404
        encrypted_pw = encrypt_string(password + salt)
        stored_pw = db.users.find_one({'email': email}, {'password': 1})
        if not stored_pw:
            return { 'reason': 'Email not registered' }, 404
        if encrypted_pw == stored_pw:
            return dumps(db.users.find({'email': email, 'password': encrypted_pw}, {'user_id': 1}))
        else:
            return { 'reason': 'Invalid password' }, 404

class User(Resource):
    def get(self, user_id=None):
        db = getDB()
        if user_id:
            # return user information
            pass
        else:
            # return all users
            return dumps(db.users.find())

    def put(self, id=None):
        #signup with user information
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        salt = bcrypt.gensalt()
        pw = encrypt_string(password + salt)
        type = data['type']
        points = 0
        streak = 0
        medications = []
        friends = []

        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': pw,
            'type': type,
            'points': points,
            'streak': streak,
            'medications': medications,
            'friends': friends
        }
        response = db.users.insert_one(new_user)
        if response.acknowledged:
            return new_user, 200
        else:
            return { 'reason': 'invalid data' }, 404


class Medication(Resource):
    pass
