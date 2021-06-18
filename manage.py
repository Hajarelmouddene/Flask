#Configure Flask CLI tool to run and manage the app from the command line

from flask.cli import FlaskGroup

from src import app

#Flaskgroup is a special command that supports loading more commands from the Flask app.
# Create a new instance of FlaskGroup to extend the normal CLI with commands related to the Flask app.
cli = FlaskGroup(app)

if __name__=='__main__':
    cli()