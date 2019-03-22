import sqlite3
import os

class Article:

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
    db_name = os.environ.get('DB_NAME') or 'database'

    def init(self):
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.db = self


class DatabaseMixin(Database):

    def __init__(self):
        self.init()
        self.crete_table()
        super().__init__()

    def clear_db(self):
        self.c.execute('DELETE FROM articles')
        self.conn.commit()

    def drop_table(self):
        self.c.execute('DROP TABLE IF EXISTS articles')

    def crete_table(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS articles "
                  "(title TEXT NOT NULL, "
                   "subtitle TEXT , "
                  "article TEXT NOT NULL, "
                  "date DATETIME NOT NULL, "
                  "image VARCHAR(244), "
                  "id INTEGER PRIMARY KEY AUTOINCREMENT)")


    def create_article(self, title, subtitle, image, article, date):
        self.c.execute('INSERT INTO articles(title, subtitle, article, date, image) values (?, ?, ?, ?, ?)',
                                                                (title, subtitle, article, date, image))
        self.conn.commit()



    def get_articles(self):
        return [self.get_obj(*q) for q in self.c.execute('SELECT * FROM articles')]

    def get_article(self, id):
        data = self.c.execute('SELECT * FROM articles WHERE id=?', (str(id), )).fetchone()
        return self.get_obj(*data) if data else None

    @property
    def get_obj(self):
        return Article


