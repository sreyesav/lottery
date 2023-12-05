from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import LotteryTicket, TicketSales, Lottery, User
from . import db
import json
from io import BytesIO
from flask import make_response
import barcode
from barcode.writer import ImageWriter

views = Blueprint('views', __name__)

def calculate_winning_amount(winning_numbers, ticket_numbers, price):
    num_matches = sum(1 for num in ticket_numbers if num in winning_numbers)

    if num_matches == 5:
        return price  # 100% winning amount
    elif num_matches == 4:
        return price * 0.2  # 20% winning amount
    elif num_matches == 3:
        return price * 0.05  # 5% winning amount
    elif num_matches == 2:
        return price * 0.01  # 1% winning amount
    else:
        return 0  # No winning amount

@views.route('/admin', methods=['POST', 'GET'])
def admin():
    latest_sale = TicketSales.query.order_by(TicketSales.id.desc()).first()
    total_tickets = latest_sale.total_tickets if latest_sale else 0
    lotteries = Lottery.query.all()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            id = request.form.get('id')
            lottery = Lottery.query.filter_by(id=id).first()
            db.session.delete(lottery)
            db.session.commit()
            flash('Lottery deleted successfully!', category='success')
            return redirect(url_for('views.home'))

        if action == 'add':
            name = request.form.get('name')
            description = request.form.get('description')
            image_url = request.form.get('image_url')
            cost = request.form.get('cost')
            winning_number1 = request.form.get('winning_number1')
            winning_number2 = request.form.get('winning_number2')
            winning_number3 = request.form.get('winning_number3')
            winning_number4 = request.form.get('winning_number4')
            winning_number5 = request.form.get('winning_number5')
            winning_amount = request.form.get('winning_amount')
            

            new_lottery = Lottery(
                name=name,
                description=description,
                img=image_url,
                cost=cost,
                winning_number1=winning_number1,
                winning_number2=winning_number2,
                winning_number3=winning_number3,
                winning_number4=winning_number4,
                winning_number5=winning_number5,
                winning_amount=winning_amount
            )
            db.session.add(new_lottery)
            db.session.commit()
            flash('Lottery added successfully!', category='success')
            return redirect(url_for('views.home'))

        if action == 'edit':
            id = request.form.get('id')
            lottery = Lottery.query.filter_by(id=id).first()

            name = request.form.get('name')
            description = request.form.get('description')
            image_url = request.form.get('image_url')
            cost = request.form.get('cost')
            winning_number1 = request.form.get('winning_number1')
            winning_number2 = request.form.get('winning_number2')
            winning_number3 = request.form.get('winning_number3')
            winning_number4 = request.form.get('winning_number4')
            winning_number5 = request.form.get('winning_number5')
            winning_amount = request.form.get('winning_amount')

            lottery.name = name
            lottery.description = description
            lottery.img = image_url
            lottery.cost = cost
            lottery.winning_number1 = winning_number1
            lottery.winning_number2 = winning_number2
            lottery.winning_number3 = winning_number3
            lottery.winning_number4 = winning_number4
            lottery.winning_number5 = winning_number5
            lottery.winning_amount = winning_amount

            db.session.commit()
            flash('Lottery updated successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('admin.html', total_tickets=total_tickets, lotteries=lotteries, user=current_user)


@views.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        num_tickets = int(request.form.get("num_tickets"))
        payment_method = request.form.get("payment_method")
        card = request.form.get("card") #Not using
        name_on_card = request.form.get("name-on-card")#Not using
        cvv = request.form.get("cvv")#Not using
        expiration_date = request.form.get("expiration-date")#Not using
        price = float(request.form.get("price"))  # Assuming price is a float
        lottery_id = int(request.form.get("lottery_id"))
        drawing_date = request.form.get("drawing_date")

        # increases sales 
        latest_sale = TicketSales.query.order_by(TicketSales.id.desc()).first()
        latest_sale = latest_sale.total_tickets
        num_tickets += latest_sale
        ticket_sale = TicketSales(total_tickets=num_tickets)
        db.session.add(ticket_sale)
        db.session.commit()

        # Retrieve user numbers
        number1 = int(request.form.get("winning_number1"))
        number2 = int(request.form.get("winning_number2"))
        number3 = int(request.form.get("winning_number3"))
        number4 = int(request.form.get("winning_number4"))
        number5 = int(request.form.get("winning_number5"))

        ticket_numbers =[
            number1,
            number2,
            number3,
            number4,
            number5,
            ]
        
        lottery = Lottery.query.get(lottery_id)

        # Retrieve winning numbers
        if lottery:
            Good_number1 = lottery.winning_number1
            Good_number2 = lottery.winning_number2
            Good_number3 = lottery.winning_number3
            Good_number4 = lottery.winning_number4
            Good_number5 = lottery.winning_number5
            winning_amount = lottery.winning_amount
        

        winning_numbers =[
            Good_number1,
            Good_number2,
            Good_number3,
            Good_number4,
            Good_number5
        ]

        for _ in range(num_tickets):
            lottery_ticket = LotteryTicket(
                winning_number1=number1,
                winning_number2=number2,
                winning_number3=number3,
                winning_number4=number4,
                winning_number5=number5,
                drawing_date=drawing_date,
                price=price,
                winning_amount = calculate_winning_amount(winning_numbers, ticket_numbers, winning_amount),
                user_id=current_user.id  # Assuming you have a current_user variable from Flask-Login
            )
            db.session.add(lottery_ticket)
            db.session.commit()
            flash(f'Tickets purchased successfully!', 'success')
            return redirect(url_for('views.home'))  


    lottery_id = request.args.get('lottery_id')
    num_tickets = request.args.get('num_tickets', 1, type=int)

    lottery = Lottery.query.get(lottery_id)

    return render_template('checkout.html', lottery=lottery, num_tickets=num_tickets, payment_method=payment_method, user=current_user)



@views.route('/lottery', methods=['GET', 'POST'])
@login_required
def lottery():
    
    lottery_id = request.args.get('lottery_id')


    title = request.args.get('title')
    if title:
        lottery = Lottery.query.filter_by(title=title).first()
        if lottery:
            return redirect(url_for('views.lottery', lottery_id=lottery.id))
        else:
            flash('lottery not found', category='error')

    # Query database for lottery details based on lottery_id
    
    lottery = Lottery.query.get(lottery_id)
    return render_template("lottery.html", lottery=lottery, user=current_user, lottery_id=lottery.id)


@views.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    lotteries = Lottery.query.all()  # Fetch all lotteries from the database
    return render_template("catalog.html", lotteries=lotteries, user=current_user)




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
