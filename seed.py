from app import create_app, db
from app.models import Aircraft, Route, Flight
from datetime import datetime, timedelta, time

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    #Planes
    # SyberJet SJ30i, Cirrus SF50, HondaJet Elite
    sj30 = Aircraft(name = "SyberJet SJ30i", capacity = 6)
    cirrus1 = Aircraft(name = "Cirrus SF50 Jet 1", capacity = 4)
    cirrus2 = Aircraft(name = "Cirrus SF50 Jet 2", capacity = 4)
    hondajet1 = Aircraft(name = "HondaJet Elite 1", capacity = 5)
    hondajet2 = Aircraft(name = "HondaJet Elite 2", capacity = 5)

    db.session.add_all([sj30, cirrus1, cirrus2, hondajet1, hondajet2])
    db.session.flush()

    #Routes + Prices
    #NZNE = New Zealand North East, YMML = Mel, NZRO = Rotorua, NZGB = GBI, NZCI = Chat, NZTL = tekapo
    routes = [
        #Melbhourne
        Route (origin="NZNE", destination="YMML", aircraft_id=sj30.id, price = 1000),
        #Rotorua
        Route (origin="NZNE", destination="NZRO", aircraft_id=cirrus1.id, price = 400),
        #Great barrier island
        Route (origin="NZNE", destination="NZGB", aircraft_id=cirrus2.id, price = 400),
        #chatham island
        Route (origin="NZNE", destination="NZCI", aircraft_id=hondajet1.id, price = 600),
        #lake tekapo
        Route (origin="NZNE", destination="NZTL", aircraft_id=hondajet2.id, price = 600),
    ]
    
    db.session.add_all(routes)
    db.session.commit()
    print("Database seeded with planes and routes and prices.")

    #-------------------------- Flights -----------------------------------
    today = datetime.today().date() #defined for all flights    
    flight_count = 100

    #Melbourne flights
    #Outbound from DF friday mid-morn w return from Mel on Sunday mid-aftern
    melbourne_route = Route.query.filter_by(destination="YMML").first()    

    for i in range(14):  #For 14 days
        date = today + timedelta(days=i)
        weekday = date.strftime("%A")
        if weekday == "Friday":
            db.session.add(Flight(
                route_id=melbourne_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="10:30",
                arrival_time="14:00",
                seats_left=6,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Melbourne outbound flight added for: {date} (Friday)| DF{flight_count}")
        elif weekday == "Sunday":
            db.session.add(Flight(
                route_id=melbourne_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="14:00",
                arrival_time="18:30",
                seats_left=6,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Melbourne return flight added for: {date} (Sunday)| DF{flight_count}")

    #Rotorua flights
    #Twice a day M-F, first flight from DF in morning, soon returning from Rot leaves. Second from DF late afternoon w Rot in evening
    rotorua_route = Route.query.filter_by(destination="NZRO").first()
    #today = datetime.today().date() - not needed

    for i in range(14):
        date = today + timedelta(days=i)
        weekday = date.strftime("%A")

        if weekday in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            db.session.add(Flight(
                route_id=rotorua_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="07:00",
                arrival_time="08:00",
                seats_left=4,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            db.session.add(Flight(
                route_id=rotorua_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="09:00",
                arrival_time="10:00",
                seats_left=4,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            db.session.add(Flight(
                route_id=rotorua_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="16:00",
                arrival_time="17:00",
                seats_left=4,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            db.session.add(Flight(
                route_id=rotorua_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="18:00",
                arrival_time="19:00",
                seats_left=4,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
        print(f"Rotorua inbound and outbound flights (x4) added for: {date} ({weekday})| DF{flight_count}")
    db.session.commit()
    print("Flights booked successfully.")

    #Great Barrier Island flights
    #outbound in morning MWF, return morning TThSat

    gbi_route = Route.query.filter_by(destination="NZGB").first()

    for i in range(14):
        date = today + timedelta(days=i)
        weekday = date.strftime("%A")

        if weekday in ["Monday", "Wednesday", "Friday"]:
            db.session.add(Flight(
                route_id=gbi_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="08:00",
                arrival_time="09:00",
                seats_left=4,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Great Barrier Islands outbound flights added for: {date} ({weekday})| DF{flight_count}")
        elif weekday in ["Tuesday", "Thursday", "Saturday"]:
            db.session.add(Flight(
                route_id=gbi_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="09:30",
                arrival_time="10:30",
                seats_left=4,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Great Barrier Islands flights added for: {date} ({weekday})| DF{flight_count}")

    #Chatham Island flights
    #twice a week, outbound TF, retrn WS
    chatham_route = Route.query.filter_by(destination="NZCI").first()

    for i in range(14):
        date = today + timedelta(days=i)
        weekday = date.strftime("%A")

        if weekday in ["Tuesday", "Friday"]:
            db.session.add(Flight(
                route_id=chatham_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="06:00",
                arrival_time="08:45",  # longer trip
                seats_left=5,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Chatham outbound flight added for: {date} ({weekday})| DF{flight_count}")
        elif weekday in ["Wednesday", "Saturday"]:
            db.session.add(Flight(
                route_id=chatham_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="09:30",
                arrival_time="12:15",
                seats_left=5,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Chatham return flight added for: {date} ({weekday})| DF{flight_count}")

    #Lake Tekapo flights
    #weekly outbound M, return F
    tekapo_route = Route.query.filter_by(destination="NZTL").first()

    for i in range(14):
        date = today + timedelta(days=i)
        weekday = date.strftime("%A")

        if weekday == "Monday":
            db.session.add(Flight(
                route_id=tekapo_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="10:00",
                arrival_time="11:30",
                seats_left=5,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Tekapo outbound flight added for: {date} (Monday)| DF{flight_count}")
        elif weekday == "Tuesday":
            db.session.add(Flight(
                route_id=tekapo_route.id,
                date=date.strftime("%Y-%m-%d"),
                departure_time="13:00",
                arrival_time="14:30",
                seats_left=5,
                flight_number = f"DF{flight_count + i}"
            ))
            flight_count += 1
            print(f"Tekapo return flight added for: {date} (Tuesday)| DF{flight_count}")
