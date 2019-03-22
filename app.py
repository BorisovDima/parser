from flask import Flask, render_template, request, abort
from flask.views import MethodView

from db import DatabaseMixin
from parser import Parser

import os


class IndexView(DatabaseMixin, MethodView):

    def get(self, *args, **kwargs):
        articles = self.db.get_articles()
        return render_template('index.html', articles=articles)

    def post(self, *args, **kwargs):
        self.db.clear_db()
        parser = Parser()
        for page in parser:
            self.db.create_article(*page)
        articles = self.db.get_articles()
        return render_template('index.html', articles=articles)


class DetailView(DatabaseMixin, MethodView):

    def get(self, *args, **kwargs):
        article = self.db.get_article(kwargs['id'])
        if not article:
            abort(404)
        return render_template('detail.html', article=article)


def make_app():
    app = Flask(__name__, template_folder='templates')
    app.config['DEBUG'] = os.environ.get('DEBUG') or False

    app.add_url_rule(rule='/', view_func=IndexView.as_view('index'))
    app.add_url_rule(rule='/detail/<id>/', view_func=DetailView.as_view('detail'))

    return app

