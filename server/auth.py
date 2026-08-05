import functools

from click import confirm
from flask import Blueprint, session, request, url_for, redirect, g, render_template

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    elif request.method == 'POST':
        username, password, confirm_password = [
            request.form.get(x) for x in ['username', 'password', 'passwordconfirm']
        ]

        from .database import get_db
        db = get_db()

        db.execute("INSERT INTO users (\"username\", \"password\") VALUES (%s, %s)", (username, password))
        db.commit()
        print('did this do sumn')

        return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login(errors=[]):
    if request.method == 'GET':
        return render_template('auth/login.html', errors=errors)

    elif request.method == 'POST':
        username, password = request.form['username'], request.form['password']

        from .database import get_db
        db = get_db()

        row = db.execute('SELECT * FROM users WHERE username = %s;', (username, )).fetchone()

        if password == row['password']:
            return redirect(url_for('home'))
        else:
            return 'Not logged in :('
