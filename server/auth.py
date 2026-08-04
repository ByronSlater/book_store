import functools

from flask import Blueprint, session, request, url_for, redirect, g, render_template

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html', errors=request.args.get('errors', []))

    elif request.method == 'POST':
        return redirect(url_for('auth.register', errors=['BIIG PROBLEM']))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'LOGIN'
