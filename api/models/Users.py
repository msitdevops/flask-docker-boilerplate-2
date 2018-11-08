from flask_login import UserMixin
from .base import db
from api.core import Mixin


class Users(db.Model, Mixin):
    """Users Table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self, username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<Username {self.username}>\
        <Email {self.email}><Password {self.password}>"
