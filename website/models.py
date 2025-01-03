from . import db
from flask_login import UserMixin

class FridgeItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  qty = db.Column(db.Integer)
  category = db.Column(db.String(150))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  full_name = db.Column(db.String(150))
  fridge_items = db.relationship('FridgeItem')
