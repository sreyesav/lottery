from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

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
    notes = db.relationship('Note')
    
    def __init__(self, first_name: str, email: str, password: str):
        self.first_name = first_name
        self.email = email
        self.password = password
    
    @staticmethod
    def create(first_name, email, password):
        new_user = User(first_name, email, password)
        db.session.add(new_user)
        db.session.commit()
     #can be changed to a movie review
    #Add address, phone number, and last name
    #change to customer
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #movie = db.relationship("Movie")
    #customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    #screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'))
    seat_count = db.Column(db.Integer, default=0) # 200 seats


"""
class Customer(db.Model): #not sure if we need this. we could change this to admin
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    last_name = db.Column(db.String(150))
    bookings = db.relationship('Booking')

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

class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    director = db.Column(db.String(150))
    release_date = db.Column(db.DateTime(timezone=True))
    runtime = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    description = db.Column(db.String(10000))
    rating = db.Column(db.Float)
    screenings = db.relationship('Screening')

"""