#Dairy Flat Airline Booking System

A web application for booking flights with Dairy Flat Airlines.

## Features
- Search available flights by date, origin, and destination
- Book a flight by entering passenger details
- View and cancel bookings via confirmation code
- Fully seeded with flight data for testing

## Technologies Used
- Python 3.9+
- Flask
- Flask SQLAlchemy
- SQLite
- Docker

--------------

## Getting Started

### Run with Docker

1. Build the image:

```bash
docker build -t airline_site_sim .
```

2. Run the container:

```bash
docker run -p 5000:5000 airline_site_sim
```

3. Visit `http://localhost:5000` in your browser.

> Note: If using Windows, make sure Docker Desktop is running.

### 🧪 Seeding the Database
Before running, seed the database with test flights:

```bash
python seed.py
```

This creates a `dairyflat.db` file with:
- Aircrafts
- Routes
- Flights for 2 weeks
- Sample bookings

###Local Development (W/o Docker)
```bash
pip install -r reqs.txt
python seed.py
python run.py
```

Then visit `http://localhost:5000`.
