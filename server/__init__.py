import os

from flask import Flask, redirect, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_URI='postgresql://postgres:password@book_store_db/book_store',
    )

    app.config.from_prefixed_env()

    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)


    @app.route('/')
    def index():
        return redirect('/home')

    @app.route('/home')
    def home():
        return render_template('home.html')

    return app
