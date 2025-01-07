import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app(testing=True)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user(client):
    user_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "securepassword"
    }

    response = client.post('/users', json=user_data)

    assert response.status_code == 201
    assert response.json['email'] == "testuser@example.com"
    assert response.json['full_name'] == "Test User"
    assert response.json['id'] == 1

    with client.application.app_context():
        user = User.query.filter_by(email="testuser@example.com").first()
        assert user is not None
        assert user.full_name == "Test User"
