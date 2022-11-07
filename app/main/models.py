from ..application import db
from flask_login import UserMixin

#Using the database created in application.py, we create a User class that contains an id, username, and password. We use ORM Mapping
class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)