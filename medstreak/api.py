from flask import Flask
from flask_restful import Resource, Api
import resources

app = Flask(__name__)
api = Api(app)

from views import *

api.add_resource(resources.Login, '/api/login')
api.add_resource(resources.User, '/api/user', '/api/user/<string:user_id>')
api.add_resource(resources.Medication, '/api/med', '/api/med/<string:med_id>')
api.add_resource(resources.Friends, '/api/user/<string:user_id>/friends')

if __name__ == '__main__':
    app.run(debug=True)
