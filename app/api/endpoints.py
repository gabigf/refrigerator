from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models import User, db
from flask_login import login_user

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
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
