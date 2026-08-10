import functools

from flask import Blueprint, g, redirect, render_template, request, session, url_for
from flask_bcrypt import check_password_hash, generate_password_hash
from psycopg.errors import UniqueViolation

from server.database import get_db

bp = Blueprint('auth', __name__)


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = %s;', (user_id,)
        ).fetchone()


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        error = session.get('register_error', False)
        print(f'ERROR: {error}')
        if error:
            del session['register_error']
        return render_template('auth/register.html', error=error)

    elif request.method == 'POST':
        username, password, confirm_password = [
            request.form.get(x) for x in ['username', 'password', 'passwordconfirm']
        ]

        if len(username) == 0:
            session['register_error'] = 'No username provided'
            return redirect(url_for('auth.register'))

        if len(password) == 0:
            session['register_error'] = 'No password provided'
            return redirect(url_for('auth.register'))


        print(f'username: "{username}", password="{password}", confirm="{confirm_password}"')


        if password != confirm_password:
            session['register_error'] = 'Password and confirmation did not match, please try again'
            return redirect(url_for('auth.register'))

        from .database import get_db
        db = get_db()

        password_hash = generate_password_hash(password).decode('utf-8')

        try:
            db.execute("INSERT INTO users (\"username\", \"password\") VALUES (%s, %s)", (username, password_hash))
            db.commit()
        except UniqueViolation:
            session['register_error'] = 'Username is already in use'
            return redirect(url_for('auth.register'))

        return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login_error' in session:
            del session['login_error']
            error = True
        else:
            error = False
        return render_template('auth/login.html', error=error)

    elif request.method == 'POST':
        username, password = request.form['username'], request.form['password']

        from .database import get_db
        db = get_db()

        row = db.execute('SELECT * FROM users WHERE username = %s;', (username, )).fetchone()

        if row and check_password_hash(row['password'], password):
            session.clear()
            session['user_id'] = row['id']
            return redirect(url_for('home'))
        else:
            session['login_error'] = True
            return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
