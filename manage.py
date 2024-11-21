from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app.main import app

cli = FlaskGroup(app)

cli.add_command('db', Migrate)

if __name__ == '__main__':
    cli()
