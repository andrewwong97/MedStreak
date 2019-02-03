from flask import Flask, request
from flask_restful import Resource
from bson.json_util import dumps
from database import getDB
import hashlib
import bcrypt
import uuid


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
        GET /api/users/<userid> - specific user
        GET /api/users - all users
        """
        db = getDB()
        if user_id:
            # return user information
            user = db.users.find_one({'user_id': user_id}, {'password': 0, 'salt': 0})
            if not user:
                return {'reason': 'User not found'}, 404
            return _serialize(user)
        else:
            # return all users
            user_list = [_serialize(u) for u in db.users.find()]
            return dumps(user_list)

    def post(self):
        # signup with user information
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
            return {'reason': 'Invalid data'}, 404

    def put(self):
        pass

class Medication(Resource):
    def post(self, user_id=None):
        """
        Create medication and add it to a user’s list of medications
        POST  /api/medications/{user id}
        """
        if not user_id:
            return {'reason': 'Invalid user'}, 404
        db = getDB()
        data = request.get_json()
        med_name = data['name']
        med_instr = data['instructions']
        schedule = data['schedule']
        adherence = data['adherence']
        med_id = uuid.uuid4()
        medication = {
            'med_id': med_id,
            'med_name': med_name,
            'med_instr': med_instr,
            'schedule': schedule,
            'adherence': adherence
        }
        response = db.medications.insert_one(medication)
        if response.acknowledged:
            return medication, 200
        else:
            return {'reason': 'Invalid data'}, 404

    def put(self, med_id=None):
        """
        Update adherence table for a medication
        PUT /api/medications/{med id}
        """
        if not med_id:
            return {'reason': 'Med_id not provided'}, 404
        db = getDB()
        data = request.get_json()
        adherence = data['adherence']
        medication = db.medications.find_one_and_update({'med_id': med_id}, {'$set': {'adherence': adherence}})
        if not medication:
            return {'reason': 'Invalid med id'}, 400
        return medication, 200

class Friends(Resource):
    pass