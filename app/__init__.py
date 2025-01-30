from flask import Flask
from app.extensions import db
from app.models import User
from app.api import register_blueprints
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app(testing=False):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = 'thisismysecretkeywouldyouhaveguessedit'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if testing:
      app.config["TESTING"] = True
      app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    db.init_app(app)

    migrate = Migrate(app, db)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
      with db.session() as session:
        return session.get(User, int(user_id))

    register_blueprints(app)


    return app
