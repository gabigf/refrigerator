from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify(user.to_response_json()), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    return jsonify({"error": "No user is logged in"}), 400
