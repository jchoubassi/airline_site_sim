from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Route, Flight, Booking, db
import uuid

main = Blueprint('main', __name__)

# Home page
@main.route('/')
def index():
    return render_template('index.html')

# Search page
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

# Book flight
@main.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)

    if request.method == 'POST':
        salutation = request.form.get('salutation')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        if flight.seats_left > 0:
            reference = str(uuid.uuid4())[:8]
            booking = Booking(
                flight_id=flight.id,
                salutation=salutation,
                first_name=first_name,
                last_name=last_name,
                email=email,
                reference=reference
            )
            flight.seats_left -= 1

            db.session.add(booking)
            db.session.commit()
            return render_template('confirmation.html', booking=booking, flight=flight)
        else:
            flash('No seats left for this flight.')
            return redirect(url_for('main.search'))
    return render_template('book.html', flight=flight)


# Cancel booking
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
            return render_template('cancelled.html', booking=booking)
        else:
            flash('Booking not found.')
            return redirect(url_for('main.cancel_booking'))

    return render_template('cancel.html')
