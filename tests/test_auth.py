import pytest
from flask import session, g
from bazblog.db import get_db

# after each test function, the created temporary database is destroyed.
# tests\conftest.py::14


def test_register(app, client):
    # when i run this view, render the 'register' page
    assert client.get('/auth/register').status == '200 OK'
    response = client.post(
        '/auth/register',
        data={'username': 't', 'password': 't'}
    )
    assert response.headers['Location'] == 'http://localhost/auth/login'

    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM user WHERE username = "t"',
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),  # data gotten from response are in bytes
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth, app):
    assert client.get('/auth/login').status == '200 OK'
    auth.login()
    # assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('a', 'test', b'Incorrect username'),
        ('test', 'a', b'Incorrect password'),
))
def test_login_validate_input(auth, client, username, password, message):
    response = client.post(
        '/auth/login',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
