
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


# from searchQueries import one_way_trip
current_date = datetime.now()
current_date.strftime('%m/%d/%Y')

# Load JSON data from AirportsFlightsandPrice- use your file path for this
with open('/Users/jason/PycharmProjects/131 Final/AeroQuest/Resources/AirportFlightsandPrice.json', 'r') as file:
    flights_data = json.load(file)

# defining the current date
app = Flask(__name__)

# set a secret key for the session
app.secret_key = b'the_secret'

# Configure the SQLAlchemy database URI (SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define SQLAlchemy model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User(username={self.username}, email={self.email})>'
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_number = db.Column(db.String(20), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    seat_number = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f'<Reservation(flight_number={self.flight_number}, departure_date={self.departure_date}, seat_number={self.seat_number})>'

# Create the database tables
db.create_all()

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register_user'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email address.', 'danger')
            return redirect(url_for('register_user'))

        # Create a new User instance
        new_user = User(username=username, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register_user'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email address.', 'danger')
            return redirect(url_for('register_user'))

        # Create a new User instance
        new_user = User(username=username, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

# Route for creating a reservation
@app.route('/reservation', methods=['GET', 'POST'])
def create_reservation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        flight_number = request.form['flight_number']
        departure_date_str = request.form['departure_date']
        seat_number = request.form['seat_number']

        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('create_reservation'))

        # Create a new Reservation instance
        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d %H:%M:%S')
        new_reservation = Reservation(user_id=user_id, flight_number=flight_number,
                                      departure_date=departure_date, seat_number=seat_number)

        # Add the new reservation to the database
        db.session.add(new_reservation)
        db.session.commit()

        flash('Reservation created successfully', 'success')
        return redirect(url_for('home'))

    users = User.query.all()
    return render_template('create_reservation.html', users=users)

# Route for viewing user reservations
@app.route('/reservations/<int:user_id>')
def view_reservations(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('home'))

    reservations = Reservation.query.filter_by(user_id=user_id).all()
    return render_template('view_reservations.html', user=user, reservations=reservations)


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/Cart')
def view_cart():
    cart_flights = session.get('cart', [])
    return render_template('cart.html', cart_flights=cart_flights)

@app.route('/AllRewards', methods=['POST'])
def choice_for_user():
    return render_template('rewards.html')

@app.route('/Cart', methods=['POST'])
def add_to_cart():
    cart = []
    if (request.form.get('flight_id')):

        flight_id = request.form.get('flight_id')

        if not flight_id:
            return "No flight ID received", 400

        filtered_flights = session.get('filtered_flights', [])

        for flight in filtered_flights:
            if str(flight['Flight_ID']) == flight_id:
                cart.append(flight)
                break
    else:
        flight_id1 = request.form.get('departure_flight')
        flight_id2 = request.form.get('arrival_flight')

        departure_flights = session.get('departure_filtered_flights', [])
        return_flights = session.get('return_filtered_flights', [])

        for flight in departure_flights:
            if str(flight['Flight_ID']) == flight_id1:
                cart.append(flight)
                break

        for flight in return_flights:
            if str(flight['Flight_ID']) == flight_id2:
                cart.append(flight)
                break

    session['cart'] = cart
    return render_template('cart.html', cart_flights=cart)


@app.route('/OneWayFlights', methods=['POST'])
def one_way():
    # Get user inputs from the form
    departure_date = request.form['departure_date']
    departure_airport = request.form['departure_airport']
    destination_airport = request.form['destination_airport']

    if not (departure_date):
        departure_date = 0

    filtered_flights = one_way_flights_query(departure_date, departure_airport, destination_airport)

    # Store the filtered flights in session
    session['filtered_flights'] = filtered_flights

    # Pass the query result to the HTML template for rendering
    return render_template('one_way_flights.html', flights=filtered_flights)


@app.route('/SortOneWayFlights', methods=['POST'])
def sort_one_way_flights():
    # retrieve the filtered flights from session
    filtered_flights = session.get('filtered_flights', [])

    sort_option = request.form['sort_option']  # Get sort option from form input

    # sort the flights by price based on the user's selection
    if sort_option == 'asc':
        sorted_flights = sorted(filtered_flights, key=lambda x: float(x['Price']))
    elif sort_option == 'desc':
        sorted_flights = sorted(filtered_flights, key=lambda x: float(x['Price']), reverse=True)
    elif sort_option == 'time':
        sorted_flights = sorted(filtered_flights, key=lambda x: (x['Departure_Time']))
    else:  # option in case of failure
        sorted_flights = filtered_flights

        # Pass the sorted flights to the HTML template for rendering
    return render_template('one_way_flights.html', flights=sorted_flights)


def one_way_flights_query(departure_date, departure_airport, destination_airport):
    filtered_flights = []

    # query if the user provides a date
    if departure_date != 0:
        filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Departure_Date'] == departure_date and
               (flight['Source_Airport_Code'] == departure_airport or flight[
                   'Source_Airport_Name'] == departure_airport) and
               (flight['Destination_Airport_Code'] == destination_airport or flight[
                   'Destination_Airport_Name'] == destination_airport)
        ]
    else:
        filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            # Parse the departure date string from flight data into a datetime object
            if (flight['Source_Airport_Code'] == departure_airport or flight[
                'Source_Airport_Name'] == departure_airport) and
               (flight['Destination_Airport_Code'] == destination_airport or flight[
                   'Destination_Airport_Name'] == destination_airport)
               and (departure_date_flight := datetime.strptime(flight['Departure_Date'], '%m/%d/%Y')) >= current_date
        ]
    return filtered_flights


def get_one_way_flight_id():
    # retrieve the filtered flights from session
    filtered_flights = session.get('filtered_flights', [])
    one_way_id = []

    for filtered_flight in filtered_flights:
        for flight in flights_data['AirportFlightsandPrice']:
            if filtered_flight['Flight_ID'] == flight['Flight_ID']:
                one_way_id.append(filtered_flight['Flight_ID'])

    return one_way_id


@app.route('/RoundTripFlights', methods=['POST'])
def round_trip_flights_query():
    departure_date = request.form.get('departure_date')
    departure_airport = request.form.get('departure_airport')
    destination_airport = request.form.get('destination_airport')

    if not (departure_date):
        departure_date = 0

    departure_filtered_flights, return_filtered_flights = round_trip_query(departure_date, departure_airport,
                                                                           destination_airport)
    session['departure_filtered_flights'] = departure_filtered_flights
    session['return_filtered_flights'] = return_filtered_flights

    return render_template('round_trip_flights.html', departure_flights=departure_filtered_flights,
                           arrival_flights=return_filtered_flights)


@app.route('/SortRoundTripFlights', methods=['POST'])
def sort_round_trip_flights():
    departure_flights = session.get('departure_filtered_flights', [])
    return_flights = session.get('return_filtered_flights', [])

    sort_option = request.form['sort_option']  # get sort option from form input

    # sort the flights based on the user's selection
    if sort_option == 'asc':
        sorted_departures = sorted(departure_flights, key=lambda x: float(x['Price']))
        sorted_returns = sorted(return_flights, key=lambda x: float(x['Price']))
    elif sort_option == 'desc':
        sorted_departures = sorted(departure_flights, key=lambda x: float(x['Price']), reverse=True)
        sorted_returns = sorted(return_flights, key=lambda x: float(x['Price']), reverse=True)
    elif sort_option == 'time':
        sorted_departures = sorted(departure_flights, key=lambda x: x['Departure_Time'])
        sorted_returns = sorted(return_flights, key=lambda x: x['Departure_Time'])
    else:  # option in case of failure
        sorted_departures = departure_flights
        sorted_returns = return_flights

    return render_template('round_trip_flights.html', departure_flights=sorted_departures,
                           arrival_flights=sorted_returns)


def round_trip_query(departure_date, departure_airport, destination_airport):
    departure_filtered_flights = []
    return_filtered_flights = []  # Corrected variable name

    # Query departure flights given departure date from user
    if departure_date != 0:
        departure_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Departure_Date'] == departure_date and
               (flight['Source_Airport_Code'] == departure_airport or flight[
                   'Source_Airport_Name'] == departure_airport) and
               (flight['Destination_Airport_Code'] == destination_airport or flight[
                   'Destination_Airport_Name'] == destination_airport)
        ]

        # Query arrival flights
        return_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Arrival_Date'] >= departure_date and
               (flight['Source_Airport_Code'] == destination_airport or flight[
                   'Source_Airport_Name'] == destination_airport) and
               (flight['Destination_Airport_Code'] == departure_airport or flight[
                   'Destination_Airport_Name'] == departure_airport)
        ]
        return departure_filtered_flights, return_filtered_flights
    else:
        departure_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if (flight['Source_Airport_Code'] == departure_airport or flight[
                'Source_Airport_Name'] == departure_airport) and
               (flight['Destination_Airport_Code'] == destination_airport or flight[
                   'Destination_Airport_Name'] == destination_airport)
               and datetime.strptime(flight['Departure_Date'], '%m/%d/%Y') >= current_date
        ]

        return_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if datetime.strptime(flight['Arrival_Date'], '%m/%d/%Y') >= current_date and
               (flight['Source_Airport_Code'] == destination_airport or flight[
                   'Source_Airport_Name'] == destination_airport) and
               (flight['Destination_Airport_Code'] == departure_airport or flight[
                   'Destination_Airport_Name'] == departure_airport)
               and datetime.strptime(flight['Departure_Date'], '%m/%d/%Y') >= current_date
        ]

        return departure_filtered_flights, return_filtered_flights


def get_round_trip_flight_id():
    # retrieve the flights from the session
    departure_flights = session.get('departure_filtered_flights', [])
    return_flights = session.get('return_filtered_flights', [])

    departure_id = []
    return_id = []
    # get departure id
    for departure in departure_flights:
        for flight in flights_data['AirportFlightsandPrice']:
            if departure['Flight_ID'] == flight['Flight_ID']:
                departure_id.append(departure['Flight_ID'])

    # get return id
    for Return in return_flights:
        for flight in flights_data['AirportFlightsandPrice']:
            if Return['Flight_ID'] == flight['Flight_ID']:
                return_id.append(departure['Flight_ID'])

    return departure_id, return_id


if __name__ == '__main__':
    app.run(debug=True)
