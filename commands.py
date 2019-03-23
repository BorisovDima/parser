from flask.cli import AppGroup
from db import Database
from flask import current_app

db_cli = AppGroup('db')

@db_cli.command('init')
def init_db():
    db = Database(current_app)
    db.crete_tables()
    current_app.logger.info('Tables created')
