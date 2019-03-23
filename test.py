import pytest

from flask import url_for
from app import make_app
from configs import TestConfig
from db import Database, DatabaseMixin, Article
from commands import init_db

import random
from collections import namedtuple


@pytest.fixture(scope='function')
def client():
    app = make_app(TestConfig)

    db = Database(app)
    db.crete_tables()
    app.config['TESTING'] = True
    client = app.test_client()
    client.db = db
    client.app = app
    yield client

    db.delete_db()


def test_cli(client):
    run = client.app.test_cli_runner()
    result = run.invoke(init_db)
    assert result.exit_code == 0


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200
    r = client.post('/')
    assert r.status_code == 200

def test_detail(client):
    r = client.post('/')
    assert r.status_code == 200
    with client.db.init_db():
        id = client.db.c.execute('SELECT id FROM articles DESC LIMIT 1').fetchone()[0]
        with client.app.test_request_context():
            url = url_for('detail', id=id )
        r = client.get(url)
    assert r.status_code == 200


def test_db(client):
    mixin = DatabaseMixin()
    mixin.db = client.db
    mixin.Table = Article

    def check_article(first, second):
        assert first.title == second.title
        assert first.subtitle == second.subtitle
        assert first.article == second.article
        assert first.date == second.date
        assert first.image == second.image
        assert first.id == second.id

    with mixin.db.init_db():
        with client.app.test_request_context():
            articles = {}

            # create
            like_article = namedtuple('article', ['title', 'subtitle', 'article', 'date', 'image', 'id'])

            for i in range(1, 11):
                a = mixin.create(f'title{i}', f'subtitle{i}', f'article{i}', f'date{i}', f'image{i}')
                a_ = like_article(f'title{i}', f'subtitle{i}', f'article{i}', f'date{i}', f'image{i}', i)
                check_article(a, a_)
                articles[i] = a

            # get_many
            articles_ = mixin.get_many()
            for a_ in articles_:
                a = articles[a_.id]
                check_article(a, a_)

            # get_id
            a = articles[random.randrange(1, 11)]
            a_ = mixin.get_id(a.id)
            check_article(a, a_)

            # delete_many
            articles_ = mixin.get_many()
            assert len(articles_) == 10
            mixin.delete_many()
            articles_ = mixin.get_many()
            assert len(articles_) == 0

            # Article
            obj = Article('title', 'subtitle', 'article' * 100, 'date', 'image', 1)
            assert len(obj.get_text(300)) + len(obj.title) == 300



