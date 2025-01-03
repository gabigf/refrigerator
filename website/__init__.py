from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from os import path
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'thisismysecretkeywouldyouhaveguessedit'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth)

    from .models import User, FridgeItem

    create_database(app)

    return app

def create_database(app):
  with app.app_context():
    if not path.exists('website/' + "database.db"):
      db.create_all()
      print('Created Database')
