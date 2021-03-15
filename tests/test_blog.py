
import sqlite3
import pytest
from flaskr.db import get_db

# test `load_logged_in_user, get_post`...


def test_index(client, auth):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'test\nbody' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
        '/create',
        '/1/update',
        '/1/delete',
))
def test_login_required(path, client):
    response = client.get(path)
    assert 'http://localhost/auth/login' == response.headers['Location']


@pytest.mark.parametrize('path', (
        '/1/update',
        '/1/delete',
))
def test_author_required(path, app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    assert client.get(path).status == '403 FORBIDDEN'
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
        '/2/update',
        '/2/delete',
))
def test_exists_required(path, app, client, auth):
    auth.login()
    assert client.get(path).status == '404 NOT FOUND'


def test_create(auth, client, app):
    auth.login()
    assert client.get('/create').status == '200 OK'
    response = client.post('/create', data={'title': 'Rhapsody',
                                            'body': 'An exalted or exaggerated expression'
                                                    'of feeling in speech or writing.'})
    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM post WHERE title = "Rhapsody"'
        ).fetchone() is not None

    assert response.headers['Location'] == 'http://localhost/'


# @pytest.mark.parametrize(('id', 'message'), (
#         (1, sqlite3),
#         (2, None),
# ))
# def test_get_post(client, auth, app, id, message):
#
#     with app.app_context():
#         post = get_db().execute(
#             'SELECT post.id, title, body, created, author_id, username'
#             '   FROM post JOIN user ON user.id = post.author_id'
#             '   WHERE post.id = ?', (id,)
#         ).fetchone()


def test_update(auth, app, client):

    auth.login()
    assert client.get('/1/update').status == '200 OK'
    response = client.post('/1/update', data={'title': 'Changed test title', 'body': 'new body added.'})

    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM post WHERE title = "Changed test title"'
        ).fetchone() is not None

    assert response.headers['Location'] == 'http://localhost/'


@pytest.mark.parametrize(('title', 'body', 'message'), (
        ('', 'Hey', b'Title is required'),
        ('Hey', '', b'Write a Post!'),
))
def test_update_validate(title, body, message, auth, client):
    auth.login()
    response1 = client.post('/create', data={'title': title, 'body': body})
    response2 = client.post('/1/update', data={'title': title, 'body': body})
    assert message in response1.data
    assert message in response2.data


def test_delete(app, auth, client):
    auth.login()

    response = client.get('/1/delete')

    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM post WHERE id = 1'
        ).fetchone() is None

    assert response.headers['Location'] == 'http://localhost/'
