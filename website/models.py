from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, time, timedelta

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000)) #change character limit later to 255
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    number = db.Column(db.String(150), unique=True)
    notes = db.relationship('Note')
    #Add address, phone number, and last name

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater = db.Column(db.String(150))
    showtime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #movie = db.relationship("Movie")
    #screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'))
    #ticket_count = db.Column(db.Integer, nullable=False, default=0) # 200 seats

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(10000))
    img = db.Column(db.String(1000))

class TicketSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_tickets = db.Column(db.Integer, nullable=False, default=0)


"""
class Screening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True))
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    bookings = db.relationship('Booking')

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    screenings = db.relationship('Screening')

"""
