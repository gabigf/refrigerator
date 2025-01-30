from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Item, db

items = Blueprint('items', __name__)

@items.route('/items', methods=['POST'])
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

    return jsonify(item.to_response_json()), 201
