from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models import User, Item, db
from flask_login import login_user, logout_user, current_user, login_required

api = Blueprint('api', __name__)


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password, full_name=data['full_name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_response_json()), 201



@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify(user.to_response_json()), 200
    return jsonify({'message': 'Invalid credentials'}), 401



@api.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    else:
        return jsonify({"error": "No user is logged in"}), 400



@api.route('/items', methods=['POST'])
@login_required
def add_item():
    data = request.get_json()

    if not data or not all(key in data for key in ["name", "quantity", "category"]):
        return jsonify({"message": "Invalid input"}), 400

    item = Item(
        name=data["name"],
        quantity=data["quantity"],
        category=data["category"],
        user_id=current_user.id
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({
        "id": item.id,
        "name": item.name,
        "quantity": item.quantity,
        "category": item.category,
        "user_id": item.user_id
    }), 201