from extensions import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __table_name__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    login_count = db.Column(db.Integer, default=0)
    messages = db.relationship("Messages", backref="messenger", lazy="dynamic")

class Messages(db.Model):
    __bind_key__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    message_date = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))