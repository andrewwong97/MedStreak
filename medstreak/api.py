from flask import Flask
from flask_restful import Api
import resources

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.Login, '/api/login')
api.add_resource(resources.User, '/api/user', '/api/user/<string:user_id>')
api.add_resource(resources.Friends, '/api/user/<string:user_id>/friends')
api.add_resource(resources.Medication, '/api/med/<string:user_id>')
api.add_resource(resources.Event, '/api/med/<string:user_id>/<string:med_id>/event')

if __name__ == '__main__':
    app.run(debug=True)
