from flask import Flask
from app.extensions import db, create_database
from app.models import User, Item
from app.api.endpoints import api
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = 'thisismysecretkeywouldyouhaveguessedit'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(api, url_prefix='/')


    create_database(app)
    login_manager = LoginManager(app)

    return app
