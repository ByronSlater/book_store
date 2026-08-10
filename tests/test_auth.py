from flask_bcrypt import *
from server.auth import *


def test_password_hash():
    password = 'test'

    hash = generate_password_hash(password)

    assert hash != password


def test_check_password():
    hash = generate_password_hash('test')

    assert check_password_hash(hash, 'test')


def test_create_user_hashes(test_client, db):
    test_client.post('/register', data={
        'username': 'test_user',
        'password': 'test_password'
    })

    row = db.execute('SELECT * FROM users WHERE username = %s;', ('test_user',)).fetchone()

    assert row['password'] != 'test_password'


def test_check_user_works(test_client, db):
    test_client.post('/register', data={
        'username': 'test_user',
        'password': 'test_password'
    })

    response = test_client.post('/login', data={
        'username': 'test_user',
        'password': 'test_password'
    })

    assert response.status_code == 302


def test_check_user_works_incorrect(test_client, db):
    test_client.post('/register', data={
        'username': 'test_user',
        'password': 'test_password'
    })

    response = test_client.post('/login', data={
        'username': 'test_user',
        'password': 'test_password2'
    })

    assert response.status_code != 302
