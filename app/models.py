from app import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  quantity = db.Column(db.Integer)
  category = db.Column(db.String(150))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  full_name = db.Column(db.String(150))
  items = db.relationship('Item')
  def check_password(self, password):
        return check_password_hash(self.password, password)
