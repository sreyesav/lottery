from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy import or_
from flask_login import login_required, current_user
from .models import Note, TicketSales, Movie
from . import db
import json
#import qrcode
#from io import BytesIO
#from flask_mail import Message

views = Blueprint('views', __name__)


@views.route('/edit', methods=['POST','GET'])
def edit():
    return render_template('edit.html', user=current_user)

@views.route('/admin', methods=['POST','GET'])
def admin():

    latest_sale = TicketSales.query.order_by(TicketSales.id.desc()).first()
    latest_sale = latest_sale.total_tickets

    movies = Movie.query.all()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            title = request.form.get('title')
            description = request.form.get('description')
            new_movie = Movie(title=title, description=description)
            db.session.add(new_movie)
            db.session.commit()
            flash('Movie added successfully!', category='success')

        elif action == 'edit':
            id = request.form.get('id')
            movie = Movie.query.filter_by(id=id).first()

            title = request.form.get('title')
            description = request.form.get('description')
            image_url = request.form.get('image_url')
            
            movie.title = title
            movie.description = description
            movie.img = image_url

            db.session.commit()
            flash('Movie updated successfully!', category='success')

        elif action == 'delete':
            id = request.form.get('id')
            movie = Movie.query.filter_by(id=id).first()
            
            db.session.delete(movie)
            db.session.commit()
            
            flash('Movie deleted successfully!', category='success')

    return render_template('admin.html', total_tickets=latest_sale, movies=movies, user=current_user)


@views.route('/checkout', methods=['POST','GET'])
def checkout():
    if request.method == 'POST':
        
        num_tickets = int(request.form.get("num_tickets"))
        #This grabs the latest number of tickets sold
        latest_sale = TicketSales.query.order_by(TicketSales.id.desc()).first()
        latest_sale = latest_sale.total_tickets

        num_tickets+=latest_sale
        ticket_sale = TicketSales(total_tickets=num_tickets)
        db.session.add(ticket_sale)
        db.session.commit()

        ####################STILL REQUIRES QR CODE##################### 
        flash('Purchase Complete, Check your email!', category='success')
    return render_template('checkout.html', user=current_user)
"""
###########
@views.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        return 'User not found', 404
    
    # Generate QR code image
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(str(user.id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Generate confirmation code
    confirmation_code = generate_confirmation_code()
    user.confirmation_code = confirmation_code
    db.session.commit()
    
    # Send email with confirmation code
    msg = Message('Confirmation Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your confirmation code is {confirmation_code}'
    with BytesIO() as buffer:
        img.save(buffer, 'png')
        buffer.seek(0)
        msg.attach('qrcode.png', 'image/png', buffer.getvalue())
    mail.send(msg)
    
    return 'Email sent successfully'
####### not finished
"""

@views.route('/movie', methods=['GET','POST'])
@login_required
def movie():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Comment is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Comment Added!', category='success')
    # Query database for movie details based on movie_id
    movie_id = request.args.get('movie_id')
    movie = Movie.query.get(movie_id)

    return render_template("movie.html", movie=movie, user=current_user)



@views.route('/catalog', methods=['GET', 'POST'] )
def catalog():
    query = request.args.get('query', default='')

    if query:
        movies=Movie.query.filter(Movie.title.ilike(f'%{query}%')).all()
    else:
        movies = Movie.query.all()

    return render_template("catalog.html", user=current_user, movies=movies, query=query)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #movie = Movie.query.all()
    return render_template('home.html', movie=movie, user=current_user)
    #return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    #we can manipulate the code at the bottom to only allow certain users to delete comments, such as admins
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/movies/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', category='success')
    return jsonify({'success': True})