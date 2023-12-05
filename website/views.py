from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import LotteryTicket, TicketSales, User
from . import db
import json
from io import BytesIO
from flask import make_response
import barcode
from barcode.writer import ImageWriter

views = Blueprint('views', __name__)

@views.route('/admin', methods=['POST', 'GET'])
def admin():
    latest_sale = TicketSales.query.order_by(TicketSales.id.desc()).first()
    latest_sale = latest_sale.total_tickets

    tickets = LotteryTicket.query.all()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            id = request.form.get('id')
            ticket = LotteryTicket.query.filter_by(id=id).first()
            db.session.delete(ticket)
            db.session.commit()

        if action == 'add':
            ticket_type = request.form.get('ticket_type')
            drawing_date = request.form.get('drawing_date')
            price = request.form.get('price')
            winning_amount = request.form.get('winning_amount')
            new_ticket = LotteryTicket(
                ticket_type=ticket_type,
                drawing_date=drawing_date,
                price=price,
                winning_amount=winning_amount,
                user_id=None
            )
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket added successfully!', category='success')

        if action == 'edit':
            id = request.form.get('id')
            ticket = LotteryTicket.query.filter_by(id=id).first()

            ticket_type = request.form.get('ticket_type')
            drawing_date = request.form.get('drawing_date')
            price = request.form.get('price')
            winning_amount = request.form.get('winning_amount')

            ticket.ticket_type = ticket_type
            ticket.drawing_date = drawing_date
            ticket.price = price
            ticket.winning_amount = winning_amount

            db.session.commit()
            flash('Ticket updated successfully!', category='success')

    return render_template('admin.html', total_tickets=latest_sale, tickets=tickets, user=current_user)


@views.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        num_tickets = int(request.form.get("num_tickets"))
        temp_tickets = num_tickets

        latest_sale = TicketSales.query.order_by(TicketSales.id.desc()).first()
        latest_sale = latest_sale.total_tickets

        num_tickets += latest_sale
        ticket_sale = TicketSales(total_tickets=num_tickets)
        db.session.add(ticket_sale)
        db.session.commit()

        # Step 3: Generate barcode and render it on a new page
        code128 = barcode.get('code128', (str(temp_tickets) + " " + current_user.email), writer=ImageWriter())
        buffer = BytesIO()
        code128.write(buffer)
        image_bytes = buffer.getvalue()
        response = make_response(image_bytes)
        response.headers['Content-Type'] = 'image/png'

        return response

    return render_template('checkout.html', user=current_user)


@views.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    tickets = LotteryTicket.query.all()
    return render_template("catalog.html", tickets=tickets, user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/delete-ticket', methods=['POST'])
def delete_ticket():
    ticket = json.loads(request.data)
    ticket_id = ticket['ticket_id']
    ticket = LotteryTicket.query.get(ticket_id)

    if ticket:
        db.session.delete(ticket)
        db.session.commit()

    return jsonify({})
