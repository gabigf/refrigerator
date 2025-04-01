from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models import User, db

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password, full_name=data['full_name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_response_json()), 201
