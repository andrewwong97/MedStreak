from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class users(Resource):
    def get(self):
        return ['andrew', 'jack']

api.add_resource(users, '/users')

if __name__ == '__main__':
    app.run(debug=True)