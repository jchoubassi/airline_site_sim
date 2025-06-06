from . import db
import uuid

class Aircraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(4), nullable=False)
    destination = db.Column(db.String(4), nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    departure_time = db.Column(db.String(5), nullable=False)
    arrival_time = db.Column(db.String(5), nullable=False)
    seats_left = db.Column(db.Integer, nullable=False)
    flight_number = db.Column(db.String(10), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    salutation = db.Column(db.String(10))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    reference = db.Column(db.String(10), unique=True, nullable=False)
    def __repr__(self):
        return f"<Booking {self.first_name} {self.last_name} - {self.reference}>" #for csv
