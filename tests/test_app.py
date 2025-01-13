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

@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "securepassword"
    }

@pytest.fixture
def invalid_login_data():
    return {
        "email": "testuser@example.com",
        "password": "wrongPassword"
    }

@pytest.fixture
def expected_user():
    return lambda user: {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }



def test_create_user(client, user_data, expected_user):
    response = client.post('/users', json=user_data)
    assert response.status_code == 201

    response_data = response.json
    assert response_data["email"] == user_data["email"]
    assert response_data["full_name"] == user_data["full_name"]

    with client.application.app_context():
        user = User.query.filter_by(email=user_data["email"]).first()
        assert user is not None
        assert response_data == expected_user(user)



def test_login_success(client, user_data, expected_user):
    client.post('/users', json=user_data)

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 200

    response_data = response.json
    assert response_data["email"] == user_data["email"]
    assert response_data["full_name"] == user_data["full_name"]

    with client.application.app_context():
        user = User.query.filter_by(email=user_data["email"]).first()
        assert response_data == expected_user(user)



def test_login_unsuccessful(client, user_data, invalid_login_data):
    client.post('/users', json=user_data)

    response = client.post('/login', json=invalid_login_data)
    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials"



def test_logout(client, user_data):
  # login user
    client.post('/users', json=user_data)
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    client.post('/login', json=login_data)

  # logout user
    response = client.post('/logout')
    assert response.status_code == 200
    assert response.json["message"] == "Logout successful"

  # check if user is logged out
    logout_response = client.post('/logout')
    assert logout_response.status_code == 400
    assert logout_response.json["error"] == "No user is logged in"