import os

from flask import Flask, redirect, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_URI='postgresql://byronslater@localhost:5432/book_store'
    )

    app.config.from_prefixed_env()

    from . import auth, authors, books, database
    database.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(authors.bp)
    app.register_blueprint(books.bp)


    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return redirect('/home')

    @app.route('/home')
    def home():
        return render_template('home.html')

    return app
