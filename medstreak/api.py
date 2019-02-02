from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, id=None):
        if not id == None:
            #return user information
            pass
        else:
            #return user id
            pass

    def post(self, id=None):
        #login with username/password
        pass

    def put(self, id=None):
        #signup with user information
        pass

    def patch(self, id=None)


api.add_resource(User, '/user', '/user/<id>')

class Medication(Resource):


if __name__ == '__main__':
    app.run(debug=True)
