from app import create_app
import pytest
from app.blueprints.main.models import User

@pytest.fixture
def app():
    app= create_app()
    return app

@pytest.fixture
def new_user():
    user = User(id=1, email = 'gupps@gmail.com', username='Guppy', password='abc123')
    return user