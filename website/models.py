from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class LotteryTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(10), unique=True)
    drawing_date = db.Column(db.DateTime(timezone=True))
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

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(300))

class LotteryTicketType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    cost = db.Column(db.Float)
    numbers_range = db.Column(db.String(20))

class TicketSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_tickets = db.Column(db.Integer, nullable=False, default=0)

class PurchaseHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('lottery_ticket.id'))
    date_purchased = db.Column(db.DateTime(timezone=True), default=func.now())