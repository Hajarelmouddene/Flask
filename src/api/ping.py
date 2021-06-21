from flask import Blueprint
from flask_restx import Resource, Api

# Blueprints are self-contained components, used for encapsulating code, templates, and static files.
# create a new instance of the Blueprint class and bind the ping resource to it.
ping_blueprint = Blueprint('ping', __name__)
api = Api(ping_blueprint)


#resources are built on top of Flask pluggable views. They provide easy access to HTTP methods
#just by defining methods on the resource.
#Flask-RESTX supports multiple return values: response code, response headers

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }

#add resource can be passed many URLs api.add_resource(Ping, "/ping", "/hello")
api.add_resource(Ping, '/ping')