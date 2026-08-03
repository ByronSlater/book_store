import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='postgresql://postgres:password@book_store_db/book_store',
    )

    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)


    @app.route('/test')
    def test():
        return 'Hello'

    return app
