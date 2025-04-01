from app import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  quantity = db.Column(db.Integer)
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
  category = db.relationship('Category', back_populates='items')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', back_populates='items')

  def to_response_json(self):
      return {
          'id': self.id,
          'name': self.name,
          'quantity': self.quantity,
          'category': self.category.name if self.category else None,
          'user_id': self.user_id
      }

class Category(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'user_id'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='categories')
    items = db.relationship('Item', back_populates='category', cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_response_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  full_name = db.Column(db.String(150))
  items = db.relationship('Item', back_populates='user', cascade="all, delete-orphan")
  categories = db.relationship('Category', back_populates='user', cascade="all, delete-orphan")

  def check_password(self, password):
        return check_password_hash(self.password, password)

  def to_response_json(self):
      return {
          'id': self.id,
          'email': self.email,
          'full_name': self.full_name
      }
