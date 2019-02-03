from flask import Flask, request
from flask_restful import Resource
from bson.json_util import dumps
from bson.objectid import ObjectId
from database import getDB
import hashlib
import bcrypt


def _serialize(obj):
    new_obj = obj
    for field, value in new_obj.items():
        if field == '_id':
            new_obj['_id'] = str(new_obj['_id'])
        elif field == 'salt':
            del new_obj['salt']
        elif field == 'password':
            del new_obj['password']
    return new_obj


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
            return {'reason': 'account already exists', 'user': _serialize(find_user)}, 404
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
            return dumps(_serialize(new_user)), 200
        else:
            return {'reason': 'Invalid data'}, 404

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
            return _serialize(db.users.find_one({'_id': ObjectId(user_id)}))
        else:
            return {'reason': 'db failed to update user object'}, 500


class Medication(Resource):
    def post(self, user_id=None):
        """
        Create medication and add it to a user's list of medications
        POST  /api/medications/{user id}
        """
        if not user_id:
            return {'reason': 'Invalid user'}, 404
        db = getDB()
        data = request.get_json(force=True)
        med_name = data['name']
        med_instr = data['instructions']
        schedule = data['schedule']
        adherence = data['adherence']
        medication = {
            'name': med_name,
            'instructions': med_instr,
            'schedule': schedule,
            'adherence': adherence
        }
        response = db.medications.insert_one(medication)
        if response.acknowledged:
            return _serialize(medication), 200
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
        data = request.get_json(force=True)
        adherence = data['adherence']
        medication = db.medications.find_one_and_update({'med_id': med_id}, {'$set': {'adherence': adherence}})
        if not medication:
            return {'reason': 'Invalid med id'}, 400
        return _serialize(medication), 200


class Friends(Resource):
    def get(self, user_id=None):
        db = getDB()
        if user_id:
            result = []
            user = db.users.find_one({'_id': ObjectId(user_id)})
            if user:
                user_friends = user['friends']
                for f_id in user_friends:
                    u = db.users.find_one({'_id': ObjectId(f_id)})
                    if u:
                        result.append(_serialize(u))
            return {'friends': result}
        else:
            return {'reason': 'user id required to add friends'}, 404

    def post(self, user_id=None):
        """
        Add one or more friends to a user's network, also add the user to each friend's network
        POST /api/user/{user id}/friends - { friends: List<UserId> }
        """
        db = getDB()
        data = request.get_json(force=True)
        if user_id:
            user = db.users.find_one({'_id': ObjectId(user_id)})
            if user and 'friends' in data:
                # add friends
                user_friends = set(user['friends'])
                for f in data['friends']:
                    find_friend = db.users.find_one({'_id': ObjectId(f)})
                    if find_friend:
                        # add friend to user friend set
                        user_friends.add(f)
                        # add user to friend's friend set
                        f_friends = set(find_friend['friends']) | {user_id}
                        db.users.update_one({'_id': ObjectId(f)}, {'$set': {'friends': list(f_friends)}})
                db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'friends': list(user_friends)}})

                added_friends = []
                for f_id in user_friends:
                    u = db.users.find_one({'_id': ObjectId(f_id)})
                    if u:
                        added_friends.append(_serialize(u))
                return {'friends': added_friends}
            else:
                return {'reason': 'user not found'}, 500
        else:
            return {'reason': 'user id required to add friends'}, 404

    def delete(self, user_id=None, friend_user_id=None):
        """
        Remove user from friend's network and friend from user's network
        DELETE /api/user/{user id}/friends/{friend user id}
        """
        pass