from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import Category, db

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_response_json() for category in categories]), 200
