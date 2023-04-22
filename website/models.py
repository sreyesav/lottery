from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000)) #change character limit later to 255
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#class Movies(db.Model):
#database for movies, id, title, director, release date, runtime, genre, description, rating

#classes to add: Theater, screening, change user to customer, booking, employees, reviews, customer activity

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #can be changed to a movie review
    #Add address, phone number, and last name
    #change to customer