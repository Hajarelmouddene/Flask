import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# import sys


# instantiate the database without parameters
db = SQLAlchemy()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set the configuration
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Check if the proper config loaded: print(app.config, file=sys.stderr)

    # set up extensions. Tell SQLalchemy to link with our app via:
    db.init_app(app)

    # register blueprints
    from src.api.ping import ping_blueprint

    app.register_blueprint(ping_blueprint)
    from src.api.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context for flask cli. The shell context processor is used to register app and db to the shell
    # this way we can work with the app context and db without having to import them directly in the shell
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
