import os
from functools import partial

base = partial(os.path.join, os.path.dirname(__file__))

class Config:
    DB_NAME = base((os.environ.get('DB_NAME') or 'database') + '.db')
    DEBUG = os.environ.get('DEBUG') or False



class TestConfig:
    DB_NAME = base('database.test')

