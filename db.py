import sqlite3
from contextlib import contextmanager
import os

from flask import current_app

class Article:
    """
    Object relational mapping our table
    """

    # Available sql commands
    create = 'INSERT INTO articles(title, subtitle, article, date, image) values (?, ?, ?, ?, ?)'
    get_id = 'SELECT * FROM articles WHERE id=?'
    get_many = 'SELECT * FROM articles'
    delete_many = 'DELETE FROM articles'

    def __init__(self, title, subtitle, article, date, image, id):
        self.title = title
        self.subtitle = subtitle
        self.article = article
        self.date = date
        self.image = image
        self.id = id

    def get_text(self, length=None):
        return self.article if not length else self.article[:length - len(self.title)]


class Database:

    def __init__(self, app):
        self.app = app

    @contextmanager
    def init_db(self):
        """
        Create connection and cursor

        with obj.init_db():
            do something with db
        """
        self.conn = sqlite3.connect(self.app.config['DB_NAME'])
        self.c = self.conn.cursor()
        try:
            yield
        finally:
            self.conn.close()

    def delete_db(self):
        # assert os.path.exists(app.config['DB_NAME'])
        os.remove(self.app.config['DB_NAME'])

    def crete_tables(self):
        with self.init_db():
            self.c.execute("CREATE TABLE IF NOT EXISTS articles "
                      "(title TEXT NOT NULL, "
                       "subtitle TEXT , "
                      "article TEXT NOT NULL, "
                      "date DATETIME NOT NULL, "
                      "image VARCHAR(244), "
                      "id INTEGER PRIMARY KEY AUTOINCREMENT)")
            self.conn.commit()



class DatabaseMixin:
    Table = None

    def dispatch_request(self, *args, **kwargs):
        """
        Start request. Only Class-Based-Views
        """
        assert self.Table is not None
        self.db = Database(current_app)
        with self.db.init_db():
            return super().dispatch_request(*args, **kwargs)

    def create(self, *args):
        """
        Create row in table
        """
        self.db.c.execute(self.Table.create, args)
        self.db.conn.commit()
        current_app.logger.info('Article create')
        return self.Table(*args, id=self.db.c.lastrowid)

    def delete_many(self):
        """
        Delete all row in table
        """
        self.db.c.execute(self.Table.delete_many)
        self.db.conn.commit()
        current_app.logger.info('Articles deleted')

    def get_many(self):
        """
        Get all row in table
        """
        return [self.Table(*q) for q in self.db.c.execute(self.Table.get_many)]

    def get_id(self, id):
        """
        Search by id
        """
        data = self.db.c.execute(self.Table.get_id, (str(id),)).fetchone()
        return self.Table(*data) if data else None


