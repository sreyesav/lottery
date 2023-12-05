from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class LotteryTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winning_number1 = db.Column(db.Integer)
    winning_number2 = db.Column(db.Integer)
    winning_number3 = db.Column(db.Integer)
    winning_number4 = db.Column(db.Integer)
    winning_number5 = db.Column(db.Integer)
    drawing_date = db.Column(db.String(10000))
    price = db.Column(db.Float)
    winning_amount = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(300))
    address = db.Column(db.String(150))
    phone_number = db.Column(db.String(20), unique=True)
    balance = db.Column(db.Float, default=0)
    tickets = db.relationship('LotteryTicket')

class Lottery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    cost = db.Column(db.Float)
    description = db.Column(db.String(10000))
    img = db.Column(db.String(1000))
    winning_number1 = db.Column(db.Integer)
    winning_number2 = db.Column(db.Integer)
    winning_number3 = db.Column(db.Integer)
    winning_number4 = db.Column(db.Integer)
    winning_number5 = db.Column(db.Integer)
    winning_amount = db.Column(db.Float)
    drawing_date = db.Column(db.String(10000)) 

    
class TicketSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_tickets = db.Column(db.Integer, nullable=False, default=0)
