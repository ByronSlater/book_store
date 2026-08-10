from flask import Blueprint, g, redirect, render_template, request, session, url_for

from server.auth import get_db

bp = Blueprint('books', __name__)


@bp.route('/books')
def books():
    db = get_db()

    books = db.execute('SELECT books.*, authors.name FROM books JOIN authors ON books.author_id = authors.id;').fetchall()

    return render_template('books/books.html', books=books)
