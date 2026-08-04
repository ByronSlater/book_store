import functools

from flask import Blueprint, session, request, url_for, redirect, g, render_template

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html', errors=request.args.get('errors', []))

    elif request.method == 'POST':
        return redirect(url_for('auth.register', errors=['BIG PROBLEM']))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html', errors=request.args.getlist('errors'))

    elif request.method == 'POST':
        return redirect(url_for('auth.login', errors=['INVALID LOGIN']))
