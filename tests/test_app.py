import pytest
from app import create_app, db
from app.models import User, Item

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

def register_and_login(client, user_data):
    client.post("/api/users", json=user_data)
    client.post("/api/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })

def test_create_user(client, user_data, expected_user):
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201

    response_data = response.json
    assert response_data["email"] == user_data["email"]
    assert response_data["full_name"] == user_data["full_name"]

    with client.application.app_context():
        user = User.query.filter_by(email=user_data["email"]).first()
        assert user is not None
        assert response_data == expected_user(user)

def test_login_success(client, user_data, expected_user):
    client.post("/api/users", json=user_data)
    response = client.post("/api/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert response.status_code == 200
    response_data = response.json

    with client.application.app_context():
        user = User.query.filter_by(email=user_data["email"]).first()
        assert response_data == expected_user(user)

def test_login_unsuccessful(client, user_data, invalid_login_data):
    client.post("/api/users", json=user_data)
    response = client.post("/api/login", json=invalid_login_data)
    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials"

def test_logout(client, user_data):
    register_and_login(client, user_data)

    response = client.post("/api/logout")
    assert response.status_code == 200
    assert response.json["message"] == "Logout successful"

    response = client.post("/api/logout")
    assert response.status_code == 400
    assert response.json["error"] == "No user is logged in"

def test_add_item(client, user_data):
    register_and_login(client, user_data)

    item_data = {
        "name": "Milk",
        "quantity": 2,
        "category": "Dairy"
    }

    response = client.post("/api/items", json=item_data)
    assert response.status_code == 201

    response_data = response.json
    assert response_data["name"] == item_data["name"]
    assert response_data["quantity"] == item_data["quantity"]
    assert response_data["category"].lower() == item_data["category"].lower()

    with client.application.app_context():
        user = User.query.filter_by(email=user_data["email"]).first()
        item = Item.query.filter_by(name=item_data["name"], user_id=user.id).first()
        assert item is not None
        assert item.name == item_data["name"]
        assert item.quantity == item_data["quantity"]
        assert item.category.name.lower() == item_data["category"].lower()

def test_get_items_returns_user_items_only(client, user_data):
    register_and_login(client, user_data)

    item_1 = {"name": "Bread", "quantity": 1, "category": "Bakery"}
    item_2 = {"name": "Juice", "quantity": 2, "category": "Drinks"}

    client.post("/api/items", json=item_1)
    client.post("/api/items", json=item_2)

    response = client.get("/api/items")
    assert response.status_code == 200
    items = response.json

    assert len(items) == 2

    names = [item["name"] for item in items]
    assert "Bread" in names
    assert "Juice" in names


def test_get_items_excludes_other_users_items(client, user_data):
    register_and_login(client, user_data)
    client.post("/api/items", json={"name": "Butter", "quantity": 1, "category": "Dairy"})

    client.post("/api/logout")

    second_user = {
        "email": "second@example.com",
        "full_name": "Second User",
        "password": "secondpass"
    }
    register_and_login(client, second_user)
    client.post("/api/items", json={"name": "Eggs", "quantity": 12, "category": "Breakfast"})

    response = client.get("/api/items")
    assert response.status_code == 200
    items = response.json
    assert len(items) == 1
    assert items[0]["name"] == "Eggs"

