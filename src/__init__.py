from flask import Flask, jsonify
from flask_restx import Resource, Api

# instantiate app

app = Flask(__name__)

api = Api(app)


# set the configuration
app.config.from_object('src.config.DevelopmentConfig')


#resources are built on top of Flask pluggable views. They provide easy access to HTTP methods
#just by defining methods on the resource.
#Flask-RESTX supports multiple return values: response code, response headers
class Hello(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "Hello world"
        }


#add resource can be passed many URLs api.add_resource(Ping, "/ping", "/hello")
api.add_resource(Ping, "/ping")
