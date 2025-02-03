from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Category, db

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_response_json() for category in categories]), 200



@categories.route('/categories', methods=['POST'])
@login_required
def create_category():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"message": "Invalid input"}), 400

    category_exists = Category.query.filter_by(name=data["name"], user_id=current_user.id).first()
    if category_exists:
        return jsonify({"message": "Category already exists"}), 400

    category = Category(name=data["name"], user_id=current_user.id)

    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_response_json()), 201