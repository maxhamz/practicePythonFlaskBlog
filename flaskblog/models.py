from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from marshmallow import fields, Schema

# additions @ postgresql



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


    # # constructor
    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"





class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # constructor
    # def __init__ (self, title, content):
    #     self.title = title
    #     self.content = content
    #     # self.user_id = user_id

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# add this new class
class PostSchema(Schema):
  """
  Post Schema
  """
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  contents = fields.Str(required=True)
  user_id = fields.Int(required=True)
  date_posted = fields.DateTime(dump_only=True)


# add this class
class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  email = fields.Email(required=True)
  image_file = fields.Str(required=True)
  password = fields.Str(required=True)
  posts = fields.Nested(PostSchema, many=True)