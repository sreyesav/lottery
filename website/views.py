from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy import or_
from flask_login import login_required, current_user
from .models import Note, TicketSales, Movie
from . import db
import json
from io import BytesIO
from flask import make_response
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from barcode.writer import ImageWriter
views = Blueprint('views', __name__)

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
        # Step 3: Generate barcode and render it on a new page
        flash('Purchase Complete, Check your email!', category='success')

        code128 = barcode.get('code128', (str(num_tickets) + " " + current_user.email) , writer=ImageWriter())
        buffer = BytesIO()
        code128.write(buffer)
        image_bytes = buffer.getvalue()
        response = make_response(image_bytes)
        response.headers['Content-Type'] = 'image/png'
        
        return response
        
    return render_template('checkout.html', user=current_user)


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

    try:
        if query:
            movies=Movie.query.filter(Movie.title.ilike(f'%{query}%')).all()
        else:
            movies = Movie.query.all()

        return render_template("catalog.html", user=current_user, movies=movies, query=query)

    except Exception as e:
        # Print the error to the console for debugging
        print(e)
        return "An error occurred while loading the catalog."
    
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

@views.route('/admin/delete_movie/<int:id>', methods=['POST'])
@login_required
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', category='success')
    return render_template('admin.html')