from flask import Flask, request
from flask_restful import Resource
from bson.json_util import dumps
from bson.objectid import ObjectId
from database import getDB
import hashlib
import bcrypt


def _serialize(obj):
    for field in obj:
        if field == '_id':
            obj['_id'] = str(obj['_id'])
    return obj


class Login(Resource):
    def post(self):
        """
        Login with email/password, return user id on success
        POST /api/login
        """
        db = getDB()
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        salt = db.users.find_one({'email': email}, {'salt': 1})
        # check user exists
        if not salt['salt']:
            return {'reason': 'Email not registered'}, 404
        encrypted_pw = hashlib.sha256(password + salt['salt']).hexdigest()

        stored_pw = db.users.find_one({'email': email}, {'password': 1})
        if not stored_pw['password']:
            return {'reason': 'Email not registered'}, 404
        if encrypted_pw == stored_pw['password']:
            user = db.users.find_one({'email': email, 'password': encrypted_pw}, {'user_id': 1})
            if user:
                return _serialize(user)
        else:
            return {'reason': 'Invalid password'}, 404


class User(Resource):
    def get(self, user_id=None):
        """
        With user id, return full user object
        GET /api/user/<userid> - specific user
        GET /api/user - all users
        """
        db = getDB()
        if user_id:
            # return user information
            user = db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0, 'salt': 0})
            if not user:
                return {'reason': 'User not found'}, 404
            return _serialize(user)
        else:
            # return all users
            user_list = [_serialize(u) for u in db.users.find()]
            return dumps(user_list)

    def post(self):
        # signup with user information
        """
        Signup with user information
        POST /api/user - accept user dict with first_name, last_name, email, password, type
        """
        db = getDB()
        data = request.get_json(force=True)
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        find_user = db.users.find_one({'email': email})
        if find_user:
            return {'reason': 'account already exists'}, 404
        password = data['password']
        salt = bcrypt.gensalt()
        pw = hashlib.sha256(password + salt).hexdigest()
        user_type = data['type']  # patient, support, or physician
        points = 0
        streak = 0
        medications = []
        friends = []

        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'salt': salt,
            'password': pw,
            'type': user_type,
            'points': points,
            'streak': streak,
            'medications': medications,
            'friends': friends
        }
        response = db.users.insert_one(new_user)
        if response.acknowledged:
            return dumps(new_user), 200
        else:
            return {'reason': 'invalid data'}, 404

    def put(self, user_id=None):
        """
        Update with partial or full user information. Changes only the fields that differ between old and new user.
        Does not update list fields, handled in other endpoints for managing code complexity between object relations.
        PUT /api/user - accept user dict
        """
        db = getDB()
        if not user_id:
            return {'reason': 'user id required for updates'}, 404
        existing = db.users.find_one({'_id': ObjectId(user_id)})
        if not existing:
            return {'reason': 'user does not exist for id ' + user_id}, 404

        data = request.get_json(force=True)

        first_name = data['first_name'] if 'first_name' in data else existing['first_name']
        last_name = data['last_name'] if 'last_name' in data else existing['last_name']
        email = data['email'] if 'email' in data else existing['email']

        # change password
        if 'password' in data:
            password = hashlib.sha256(data['password'] + existing['salt']).hexdigest()
        else:
            password = existing['password']
        user_type = data['type'] if 'type' in data else existing['type']
        points = data['points'] if 'points' in data else existing['points']
        streak = data['streak'] if 'streak' in data else existing['streak']
        updated_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'type': user_type,
            'points': points,
            'streak': streak,
        }
        updated = db.users.update_one({
            '_id': ObjectId(user_id)
        }, {'$set': updated_user})

        if updated.acknowledged:
            return dumps(_serialize(db.users.find_one({'_id': ObjectId(user_id)})))
        else:
            return {'reason': 'db failed to update user object'}, 500



class Medication(Resource):
    pass
