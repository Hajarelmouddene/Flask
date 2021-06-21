#Configure Flask CLI tool to run and manage the app from the command line

import sys 

from flask.cli import FlaskGroup

from src import create_app, db
from src.api.models import User

app = create_app()

#Flaskgroup is a special command that supports loading more commands from the Flask app.
# Create a new instance of FlaskGroup to extend the normal CLI with commands related to the Flask app.
cli = FlaskGroup(create_app=create_app)

# register new command, recreate_db, to the CLI, so we can run it from the command line (apply model to db)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()



if __name__=='__main__':
    cli()
