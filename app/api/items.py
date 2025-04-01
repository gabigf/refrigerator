from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Item, Category, db

items = Blueprint('items', __name__)

@items.route('/items', methods=["GET"])
@login_required
def get_items():
  items = Item.query.all()
  return jsonify([item.to_response_json() for item in items]), 200

@items.route('/items', methods=['POST'])
@login_required
def add_item():
    data = request.get_json()

    if not data or not all(key in data for key in ["name", "quantity", "category"]):
        return jsonify({"message": "Invalid input"}), 400

    category_name = data["category"].strip()

    existing_category = Category.query.filter(
        Category.user_id == current_user.id,
        Category.name.ilike(category_name)
    ).first()

    if existing_category:
        category = existing_category
    else:
        category = Category(name=category_name, user_id=current_user.id)
        db.session.add(category)

    item = Item(
        name=data["name"],
        quantity=data["quantity"],
        category=category,
        user_id=current_user.id
    )
    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_response_json()), 201
