
from bazblog import create_app


def test_config():
    from os import urandom
    x = urandom(8)
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    assert create_app({'SECRET_KEY': x}).secret_key == x


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b"hello, world"
