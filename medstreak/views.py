from flask import Flask
from database import getDB
from bson.json_util import dumps
from api import app

@app.route('/login')
def login():
    return 'login'

@app.route('/foo')
def foo():
    db = getDB()
    return dumps(db.users.find())
