from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Jokes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    jokes = db.relationship('Jokes')
    memes = db.relationship('Meme')




class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(10000))  
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yt_video_id = db.Column(db.String(100))  # Store the unique YouTube video ID
    title = db.Column(db.String(1000))  # Store the user's video title
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Associate with a user


