from test.conftest import app, new_user
from app import create_app

def test_always_passes():
    assert True

def test_always_fails():
    assert False

def test_anonymous_home_page(app):
    """
    GIVEN a flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = app

    #create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Bill's PC" in response.data
        assert b"Home" in response.data
        assert b"Login" in response.data
        assert b"Register" in response.data
        # assert b"Please Login" in response.data

def test_home_post(app):
    """
    GIVEN a flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = app
    #create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405
        assert b"Bill's PC" not in response.data
        assert b"Home" not in response.data

def test_choose_pokemon(app):
    """
    GIVEN a flask application configured for testing
    WHEN the '/pokemon/choose' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = app
    #create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/pokemon/choose')