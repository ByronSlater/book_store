import os

from flask import Flask

from .database import get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='postgresql://postgres:password@book_store_db/book_store',
    )

    @app.route('/books')
    def books():
        db = get_db()

        rows = db.execute("SELECT * FROM books;")


        return [
            {**row} for row in rows
        ]

    @app.route('/authors')
    def authors():
        db = get_db()

        rows = db.execute("SELECT name, dob FROM authors;")

        return [
            {
                'name': row['name'],
                'dob': row['dob']
            }
            for row in rows
        ]

    from . import database
    database.init_app(app)

    return app
