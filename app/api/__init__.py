from flask import Blueprint
from app.api.auth import auth
from app.api.items import items
from app.api.users import users
from app.api.categories import categories

def register_blueprints(app):
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(items, url_prefix="/api")
    app.register_blueprint(users, url_prefix="/api")
    app.register_blueprint(categories, url_prefix="/api")
