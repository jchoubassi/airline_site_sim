from flask import Blueprint, render_template, request #for rendering templates
from .models import Route, Flight #for routes and flights
from .models import db #for db
from flask import redirect, url_for, flash #for flash messages
from .models import Booking #booking model
import uuid #gen booking id

main = Blueprint('main', __name__)

#home page
@main.route('/')
def index():
    return render_template('index.html')

#search page
@main.route('/search', methods=['GET', 'POST'])
def search():
    routes = Route.query.all()
    flights = []

    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        date = request.form.get('date')

        flights = Flight.query.join(Route).filter(
            Route.origin == origin,
            Route.destination == destination,
            Flight.date == date
        ).all()
    return render_template('search.html', routes=routes, flights=flights)

#book flight
@main.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)

    # Check if the flight has available seats
    if request.method == 'POST':
        name = request.form.get('name')
        
        if flight.seats_left > 0: 
            reference = str(uuid.uuid4())[:8] #ID generated
            booking = Booking(flight_id = flight.id, passenger_name = name, reference = reference)
            flight.seats_left -= 1

            db.session.add(booking)
            db.session.commit()
            return render_template('confirmation.html', booking=booking, flight=flight) # confirmation page
        else:
            flash('No seats left for this flight.')
            return redirect(url_for('main.search'))
    return render_template('book.html', flight=flight)

#cancel
@main.route('/cancel', methods=['GET', 'POST'])
def cancel_booking():
    if request.method == 'POST':
        reference = request.form.get('reference')
        booking = Booking.query.filter_by(reference=reference).first()

        if booking:
            flight = Flight.query.get(booking.flight_id)
            flight.seats_left += 1
            db.session.delete(booking)
            db.session.commit()
            return render_template('cancelled.html', booking=booking) # confirmation page
        else:
            flash('Booking not found.')
            return redirect(url_for('main.cancel_booking'))
    return render_template('cancel.html')