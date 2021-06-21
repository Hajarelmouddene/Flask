import os
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
# import sys 

# instantiate app
app = Flask(__name__)

api = Api(app)


# set the configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# Check if the proper config loaded: print(app.config, file=sys.stderr)


# instantiate the database
db = SQLAlchemy(app)


# model

class User(db.Model):
    __tablename__: 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __inti__(self, username, email):
        self.username = username
        self.email = email



#resources are built on top of Flask pluggable views. They provide easy access to HTTP methods
#just by defining methods on the resource.
#Flask-RESTX supports multiple return values: response code, response headers
class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong"
        }


#add resource can be passed many URLs api.add_resource(Ping, "/ping", "/hello")
api.add_resource(Ping, "/ping")
