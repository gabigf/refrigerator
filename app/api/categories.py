from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Category, Item, db

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify([category.to_response_json() for category in categories]), 200



@categories.route('/categories', methods=['POST'])
@login_required
def create_category():
    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"message": "Invalid input"}), 400

    category_exists = Category.query.filter(
        Category.user_id == current_user.id,
        Category.name.ilike(name)
    ).first()

    if category_exists:
        return jsonify({"message": "Category already exists"}), 400

    category = Category(name=name, user_id=current_user.id)
    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_response_json()), 201


@categories.route('/categories/<int:category_id>', methods=['PUT'])
@login_required
def edit_category(category_id):
    data = request.get_json()
    new_name = data.get('name', '').strip()

    if not new_name:
        return jsonify({"message": "Invalid input"}), 400

    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    name_exists = Category.query.filter(
        Category.user_id == current_user.id,
        Category.name.ilike(new_name),
        Category.id != category_id
    ).first()
    if name_exists:
        return jsonify({"message": "Category with this name already exists"}), 400

    category.name = new_name
    db.session.commit()

    return jsonify(category.to_response_json()), 200

@categories.route('/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    Item.query.filter_by(category_id=category.id).update({Item.category_id: None})
    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200