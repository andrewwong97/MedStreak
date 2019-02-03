from flask import Flask
from flask_restful import Resource, Api
import resources

app = Flask(__name__)
api = Api(app)

from views import *

api.add_resource(resources.Login, '/login')
api.add_resource(resources.User, '/user', '/user/<string:user_id>')
api.add_resource(resources.Medication, '/med', '/med/<string:med_id>')

if __name__ == '__main__':
    app.run(debug=True)
