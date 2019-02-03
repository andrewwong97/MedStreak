from flask import Flask, request
from flask_restful import Resource
from bson.json_util import dumps
from database import getDB
import hashlib
import bcrypt
import uuid


class Login(Resource):
    def post(self, id=None):
        """
        Login with email/password, return user id on success
        POST /api/login
        """
        db = getDB()
        data = request.get_json()
        email = data['email']
        password = data['password']
        salt = db.users.find_one({'email': email}, {'salt': 1})
        # check user exists
        if not salt:
            return {'reason': 'Email not registered'}, 404
        encrypted_pw = hashlib.sha256(password + salt)
        stored_pw = db.users.find_one({'email': email}, {'password': 1})
        if not stored_pw:
            return {'reason': 'Email not registered'}, 404
        if encrypted_pw == stored_pw:
            return dumps(db.users.find_one({'email': email, 'password': encrypted_pw}, {'user_id': 1}))
        else:
            return {'reason': 'Invalid password'}, 404


class User(Resource):
    def get(self, user_id=None):
        db = getDB()
        if user_id:
            # return user information
            user = db.users.find_one({'user_id': user_id}, {'password': 0, 'salt': 0})
            if not user:
                return {'reason': 'User not found'}, 404
            return dumps(user)
        else:
            # return all users
            return dumps(db.users.find())

    def post(self, id=None):
        # signup with user information
        db = getDB()
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        salt = bcrypt.gensalt()
        pw = hashlib.sha256(password + salt)
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
            return {'reason': 'Invalid data'}, 404


class Medication(Resource):
    def post(self, user_id=None):
        if not user_id:
            return {'reason': 'Invalid user'}, 404
        db = getDB()
        data = request.get_json()
        med_name = data['name']
        med_instr = data['instructions']
        schedule = data['schedule']
        adherence = data['adherence']
        med_id = uuid.uuid4()
        # TODO: Create Medication class
        medication = Medication(med_id, med_name, med_instr, schedule, adherence)
        db.medications.insert_one({'med_id': med_id, 'medication': medication})
        return medication

    def put(self, med_id=None):
        if not med_id:
            return {'reason': 'Med_id not provided'}, 404
        db = getDB()
        data = request.get_json()
        adherence = data.get

class Friends(Resource):
    pass