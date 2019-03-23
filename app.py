from flask import Flask, render_template, request, abort
from flask.views import MethodView
from flask.json import jsonify

from db import DatabaseMixin, Article
from parser import Parser
from cache import cache_decorator, clear_cache


class IndexView(DatabaseMixin, MethodView):
    Table = Article

    @cache_decorator(key_f=(lambda: request.full_path))
    def get(self, *args, **kwargs):
        articles = self.get_many()
        return render_template('index.html', articles=articles)

    def post(self, *args, **kwargs):
        self.delete_many()
        clear_cache()
        parser = Parser()
        articles = []
        for page in parser:
            articles.append(self.create(*page))
        return jsonify({'data': render_template('articles.html', articles=articles)})


class DetailView(DatabaseMixin, MethodView):
    Table = Article

    @cache_decorator(key_f=(lambda: request.full_path))
    def get(self, *args, **kwargs):
        article = self.get_id(kwargs['id'])
        if not article:
            abort(404)
        return render_template('detail.html', article=article)


def make_app(config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    app.add_url_rule(rule='/', view_func=IndexView.as_view('index'))
    app.add_url_rule(rule='/detail/<id>/', view_func=DetailView.as_view('detail'))

    return app







